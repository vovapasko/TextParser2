# TextParser2

Hi! To start using this program just clone this repository and go to TextParser2/ folder. You can run program using Python or special run.sh file . All necessary libraries are in requirements.txt file. If you are going to use run.sh, file will automatically set up Pyhton 3.7 virtual environment in TextParser2/venv folder, install all libraries and activate it.

If you run program on production server, you may set flag `par_datetime` in `start(par_datetime=current_datetime, write_to_server=False, send_mail=False, emergency_mode=False)` function to variable `program_start_time` like this

```python
start(par_datetime=program_start_time, write_to_server=False, send_mail=False, emergency_mode=False)
```

If you just testing this function on your PC, you may leave the configuration of start function the same. It will take as a test data mock data in test/ directory 
