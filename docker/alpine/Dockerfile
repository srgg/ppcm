FROM alpine:3.8
ENTRYPOINT ["/entrypoint.sh"]
EXPOSE 22
COPY entrypoint.sh /

# PCM requires to have suid on passwd, otherwise it will fail with 'passwd: must be suid to work properly'
RUN apk add --no-cache busybox-suid

RUN apk add --no-cache openssh \
  && sed -i s/#PermitRootLogin.*/PermitRootLogin\ yes/ /etc/ssh/sshd_config \
  && echo "root:root" | chpasswd

#RUN apk add --no-cache sudo \
#  && sed -e 's/# %wheel ALL=(ALL) NOPASSWD: ALL/%wheel ALL=(ALL) NOPASSWD: ALL/g'  -i /etc/sudoers

RUN \
  adduser -D user && \
  echo "user:user" | chpasswd


