FROM python:3.11
ENV PATH /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
RUN mkdir /project
WORKDIR /project
#
COPY ./requirements.txt /project/requirements.txt

#
RUN pip install --no-cache-dir --upgrade -r /project/requirements.txt

#

COPY ./ /project
WORKDIR /project
#COPY ./src/.env.local /api/src/.env
# команда для создание админ пользователя
#COPY ./src/BaseApi/commands/create_admin.py /usr/bin/create_admin
#COPY ./src/BaseApi/commands/change_password.py /usr/bin/change_password
#RUN chmod ugo+x /usr/bin/create_admin
#RUN chmod ugo+x /usr/bin/change_password

EXPOSE 8080
EXPOSE 8082
#
ENV PYTHONPATH "${PYTHONPATH}:/project"
RUN ls
RUN aerich migrate
RUN aerich upgrade

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
