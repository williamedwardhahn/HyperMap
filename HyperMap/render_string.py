from flask import render_template_string
render_template_string('hello {{ what }}', what='world')
