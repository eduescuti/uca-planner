import os
import sys

# Permite importar los modulos que estan en la raiz del proyecto (run, route, etc.)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from run import app  # noqa: E402

# Vercel usa esta variable `app` (WSGI) como funcion serverless.
