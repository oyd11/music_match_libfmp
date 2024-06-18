# dot me

dirname=$(basename `pwd`)
echo $dirname

# to create venv:
# python3.8 -m venv ~/.venv/$dirname

deact_if_venv() {
     deactivate 2> /dev/null
}


deact_if_venv

. ~/.venv/$dirname/bin/activate


echo \'deactivate\' to deactivate venv

