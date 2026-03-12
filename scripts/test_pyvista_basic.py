import pyvista as pv


def main():
    plotter = pv.Plotter()
    plotter.add_mesh(pv.Sphere(), color="lightblue")
    plotter.show()


if __name__ == "__main__":
    main()