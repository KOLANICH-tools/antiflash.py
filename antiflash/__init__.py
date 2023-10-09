import ast
import sys
import types
import typing
from pathlib import Path
from warnings import warn

from click.core import Command, Parameter


warn("We have moved from M$ GitHub to https://codeberg.org/KOLANICH-tools/antiflash.py, read why on https://codeberg.org/KOLANICH/Fuck-GuanTEEnomo .")

def patchSpacesBinOpAST(binOp: ast.BinOp) -> bool:
	for sideName in ("left", "right"):
		side = getattr(binOp, sideName)
		if isinstance(side, ast.Constant) and side.value == " " * 4:
			side.value = "\t"
			return True

	return False


def patchSpacesExprAST(e: ast.AST) -> bool:
	if isinstance(e, ast.Assign):
		if len(e.targets) == 1:
			t0 = e.targets[0]
			if isinstance(t0, ast.Name) and t0.id == "indent":
				v = e.value
				if isinstance(v, ast.BinOp) and isinstance(v.op, ast.Mult):
					if patchSpacesBinOpAST(v):
						return True
	return False


def patchSpacesExprWithinFuncAST(f: ast.FunctionDef) -> typing.Optional[ast.FunctionDef]:
	for el in f.body:
		if patchSpacesExprAST(el):
			return f
	return None


def patchSpacesExprWithinFuncInClassAST(c: ast.ClassDef, funcToMonkeyPatch: str) -> typing.Optional[ast.FunctionDef]:
	for el in c.body:
		if isinstance(el, ast.FunctionDef) and el.name == funcToMonkeyPatch:
			res = patchSpacesExprWithinFuncAST(el)
			if res:
				return res
	return None


def patchSpacesExprWithinFuncInClassInModuleAST(m: ast.Module, classToMonkeyPatch: str, funcToMonkeyPatch: str) -> typing.Optional[ast.FunctionDef]:
	for el in m.body:
		if isinstance(el, ast.ClassDef) and el.name == classToMonkeyPatch:
			res = patchSpacesExprWithinFuncInClassAST(el, funcToMonkeyPatch)
			if res:
				return res
	return None


def patchSpacesExprWithinFuncInClassInModule(module: types.ModuleType, classToMonkeyPatch: str, funcToMonkeyPatch: str):
	pathStr = module.__file__
	if not pathStr:
		raise ValueError("Module has no `__path__`", module)
	path = Path(pathStr)
	moduleAST = ast.parse(path.read_text("utf-8"))
	modifiedFuncAST = patchSpacesExprWithinFuncInClassInModuleAST(moduleAST, classToMonkeyPatch, funcToMonkeyPatch)
	clz = getattr(module, classToMonkeyPatch)

	globalz = dict(module.__dict__) | dict(clz.__dict__)
	monkeyPatchModule = ast.fix_missing_locations(ast.Module(body=[modifiedFuncAST], type_ignores=[]))
	exec(compile(monkeyPatchModule, "<monkey-patch of " + classToMonkeyPatch + "." + funcToMonkeyPatch + ">", "exec"), globalz)
	setattr(clz, funcToMonkeyPatch, globalz[funcToMonkeyPatch])


def applyPatch(black: types.ModuleType) -> None:
	patchSpacesExprWithinFuncInClassInModule(black.lines, "Line", "__str__")


def indexClickParams(f: Command) -> typing.Dict[str, Parameter]:
	return {el.name: el for el in f.params if el.name}


def patchDefaultParams(black: types.ModuleType, patchDict: typing.Dict[str, typing.Union[int, str]]) -> None:
	paramsIndex = indexClickParams(black.main)
	for k, v in patchDict.items():
		paramsIndex[k].default = v
