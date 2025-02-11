# if defined(__linux__)

# ifdef LIBRARY_NAME

# define PY_SSIZE_CLEAN
# include <Python.h>

# include <array>
# include <vector>
# include <ranges>

# include "../orig_algo_impl/Rasterization.hpp"


#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wunused-parameter"
static PyObject* Line(PyObject* self, PyObject* args) // Have to suppress a warning here due to the insufficiencies of the Python/C API
{
    int x_1;
    int y_1;
    int x_2;
    int y_2;

    if(!PyArg_ParseTuple(args, "iiii", &x_1, &y_1, &x_2, &y_2)) { return NULL; }

    std::vector<std::array<int, 2>> points {Rasterization::Line({{{x_1, y_1}, {x_2, y_2}}})};

    PyObject* tmp_py_tuple;
    PyObject* py_list {PyList_New(static_cast<Py_ssize_t>(points.size()))};

    for(std::size_t n {0}; n < points.size(); n++) {
        const auto& [x, y] = points[n];
        tmp_py_tuple = PyTuple_New(2);
        PyTuple_SetItem(tmp_py_tuple, 0, PyLong_FromLong(x));
        PyTuple_SetItem(tmp_py_tuple, 1, PyLong_FromLong(y));
        PyList_SetItem(py_list, static_cast<Py_ssize_t>(n), tmp_py_tuple);
    }

    return py_list;
}
#pragma GCC diagnostic pop


static PyMethodDef rasterizationMethods[] = {
    {"Line",
     Line,
     METH_VARARGS,
     NULL},
    {NULL, NULL, 0, NULL}};


PyDoc_STRVAR(rasterization_module_doc, "Python bindings for the C++ Rasterization Library");
static struct PyModuleDef rasterizationmodule = {
    PyModuleDef_HEAD_INIT,
    LIBRARY_NAME,
    rasterization_module_doc,
    -1,
    rasterizationMethods,
    NULL,
    NULL,
    NULL,
    NULL};


PyMODINIT_FUNC PyInit_Rasterization() { return PyModule_Create(&rasterizationmodule); }

# else
# error "Must define the name of the Python module to be created"
# endif

# else
# error "This file is only meant to be compiled on a Linux OS"
# endif
