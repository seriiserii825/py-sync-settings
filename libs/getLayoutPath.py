import os


def getLayoutPath(name):
    ROOT_DIR = os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
    if name == "vue":
        return f"{ROOT_DIR}/layouts/layout.vue"
    elif name == "scss":
        return f"{ROOT_DIR}/layouts/layout.scss"
    elif name == "interface":
        return f"{ROOT_DIR}/layouts/layout.interface.ts"
    elif name == "hook":
        return f"{ROOT_DIR}/layouts/layout.hook.ts"
    elif name == "api":
        return f"{ROOT_DIR}/layouts/layout.api.ts"
    elif name == "store":
        return f"{ROOT_DIR}/layouts/layout.store.ts"
    else:
        exit('Invalid layout name')
