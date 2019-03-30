from unittest import TestCase, main


class ImportTest(TestCase):
    def test_module(self):
        try:
            import marching_cubes
        except ImportError as e:
            self.fail(e)

    def test_function(self):
        try:
            from marching_cubes import march
        except ImportError as e:
            self.fail(e)


if __name__ == "__main__":
    main()
