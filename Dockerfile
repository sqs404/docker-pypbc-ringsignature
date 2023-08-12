FROM ubuntu:20.04
#
WORKDIR /app
# 换源
RUN sed -i 's#http://archive.ubuntu.com/#http://mirrors.tuna.tsinghua.edu.cn/#' /etc/apt/sources.list;
# Inital linux Liberaries
RUN apt-get -y update
RUN apt-get install -y libgmp-dev build-essential flex bison git curl python3-pip
#-------------------------------------------------------------------------------
# Install PBC
RUN curl -L https://crypto.stanford.edu/pbc/files/pbc-0.5.14.tar.gz | tar zxv
#RUN cd pbc-0.5.14 && sh ./setup
RUN cd pbc-0.5.14 && ./configure --prefix=/usr --enable-shared
RUN cd pbc-0.5.14 && make && make install && ldconfig
#-------------------------------------------------------------------------------
# Install PyPBC
RUN git clone --depth 1 https://github.com/debatem1/pypbc.git
RUN cd pypbc &&  pip3 install .

# RUN pip3 install ...
#COPY requirements.txt /app
#RUN pip install -r requirements.txt

WORKDIR /app/dev

COPY /dev/index.py /app/dev

CMD python3 index.py

