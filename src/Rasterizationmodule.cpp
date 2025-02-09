# define PY_SSIZE_CLEAN
# include <Python.h>

# include <array>
# include <vector>
# include <ranges>

# include "Rasterization.hpp"


PyDoc_STRVAR(Line_doc, "Line Rasterization Algorithm");
static PyObject* Line(PyObject* self, PyObject* args)
{
    int x_1;
    int y_1;
    int x_2;
    int y_2;

    if(!PyArg_ParseTuple(args, "iiii", &x_1, &y_1, &x_2, &y_2)) { return NULL; }

    std::vector<std::array<int, 2>> points {Rasterization::Line({{{x_1, y_1}, {x_2, y_2}}})};

    PyObject* tmp_py_tuple;
    PyObject* py_list {PyList_New(points.size())};

    for(std::size_t n {0}; n < points.size(); n++) {
        const auto& [x, y] = points[n];
        tmp_py_tuple = PyTuple_New(2);
        PyTuple_SetItem(tmp_py_tuple, 0, PyLong_FromLong(x));
        PyTuple_SetItem(tmp_py_tuple, 1, PyLong_FromLong(y));
        PyList_SetItem(py_list, static_cast<Py_ssize_t>(n), tmp_py_tuple);
    }

    return py_list;
}


static PyMethodDef rasterizationMethods[] = {
    {"Line",
     Line,
     METH_VARARGS,
     Line_doc},
    {NULL, NULL, 0, NULL}};


PyDoc_STRVAR(rasterization_module_doc, "Python bindings for the C++ Rasterization Library");
static struct PyModuleDef rasterizationmodule = {
    PyModuleDef_HEAD_INIT,
    "Rasterization",
    rasterization_module_doc,
    -1,
    rasterizationMethods};


PyMODINIT_FUNC PyInit_Rasterization() { return PyModule_Create(&rasterizationmodule); }


