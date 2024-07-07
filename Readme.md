# 1. Create a new virtual environment

python -m venv myenv

# 2. Activate the virtual environment

# On Windows:

myenv\Scripts\activate

# On macOS and Linux:

source myenv/bin/activate

# 3. Your prompt should change, indicating the active environment

# Now you can install packages isolated to this environment

pip install vobject

# 4. Verify the installation

python -c "import vobject; print(vobject.__version__)"

# 5. When you're done, you can deactivate the environment

deactivate

# 6. To use the environment again later, just activate it

# No need to recreate it

# 7. If you want to see all installed packages in the environment

pip list

# 8. To create a requirements.txt file

pip freeze > requirements.txt

# 9. To install from a requirements.txt file in a new environment

# pip install -r requirements.txt
