# define PY_SSIZE_CLEAN
# include <Python.h>
# include <iostream>

static PyObject* add(PyObject* self, PyObject* args) 
{ 
    int addend_1;
    int addend_2;
    
    if(!PyArg_ParseTuple(args, "ii", &addend_1, &addend_2)) { return NULL; }

    return PyLong_FromLong(addend_1 + addend_2);  
}


static PyMethodDef rasterizationMethods[] = {{"add",
                                              add,
                                              METH_VARARGS,
                                              "Add two integers"},
                                             {NULL, NULL, 0, NULL}};

static struct PyModuleDef rasterizationmodule = {
    PyModuleDef_HEAD_INIT,
    "rasterization",
    NULL,
    -1,
    rasterizationMethods};


PyMODINIT_FUNC PyInit_rasterization() { return PyModule_Create(&rasterizationmodule); }


