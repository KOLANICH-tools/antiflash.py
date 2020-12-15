from . import applyPatch, patchDefaultParams

defaultsPatch = {
	"line_length": (1 << 64) - 1,
}


def main():
	import black  # pylint:disable=import-outside-toplevel

	patchDefaultParams(black, defaultsPatch)
	applyPatch(black)
	black.patched_main()


if __name__ == "__main__":
	main()
