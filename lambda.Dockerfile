FROM public.ecr.aws/lambda/python:3.11

RUN yum update -y && yum upgrade -y

WORKDIR ${LAMBDA_TASK_ROOT}

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD [ "app.main.handler" ]