FROM debian:latest

RUN apt -y update && apt install -y git python3-pip python3-dev python3-tk neovim procps curl libsm6 libxext6 libxrender-dev

#Face classificarion dependencies & web application
RUN pip3 install \
pandas \
scikit-learn \
scipy==1.1.0 \
Pillow \
tensorflow==1.14.0 \
"numpy<1.17" \
h5py \
opencv-python==4.2.0.32 \
keras \
statistics \
pyyaml \
pyparsing \
cycler \
matplotlib \
Flask \
setuptools==41.0.0

WORKDIR /opt/face-classifier

COPY . .


ENV PYTHONPATH=$PYTHONPATH:src
ENV FACE_CLASSIFIER_PORT=8000
EXPOSE $FACE_CLASSIFIER_PORT

ENTRYPOINT ["python3"]

#start the server
CMD ["src/web/faces.py"]
