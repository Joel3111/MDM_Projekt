FROM python:3.12.1
# Copy Files
WORKDIR /app
COPY kalorien_model.joblib //app/kalorien_model.joblib
COPY kalorien_app kalorien_app
# Install
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
# Docker Run Command
EXPOSE 5000
ENV FLASK_APP=kalorien_app/app.py
CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0"]