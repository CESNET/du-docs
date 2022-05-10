FROM nvcr.io/nvidia/tensorflow:22.02-tf2-py3

ENV DEBIAN_FRONTEND=noninteractive 
ENV TZ=Europe/Prague

RUN apt update && apt install -y python3-notebook python3-pip wget 

RUN pip3 install jupyterhub

WORKDIR /home/jovyan
ENV HOME /home/jovyan

RUN wget https://raw.githubusercontent.com/ljocha/binder-demo2/main/img-classifier.ipynb -O /home/jovyan/img-classifier.ipynb

RUN useradd -m -u 1000 jovyan
RUN chown -R 1000:1000 /home/jovyan

CMD jupyter notebook --NotebookApp.token='' --NotebookApp.password=''
