# syntax=docker/dockerfile:1
FROM python:3

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN useradd --create-home appuser
WORKDIR /home/appuser/code

# copy requirements.txt and install dependencies
COPY --chown=appuser:appuser requirements.txt /home/appuser/code/
RUN pip install --no-cache-dir -r requirements.txt
# install gunicorn
RUN pip install gunicorn

# Copy local code to the container image.
COPY --chown=appuser:appuser . /home/appuser/code/

# Copy config file
COPY --chown=appuser:appuser config.json /home/appuser/.config/revChatGPT/config.json

# Install Oh My SH
ENV SHELL /bin/zsh
RUN apt-get update && apt-get install -y curl zsh
RUN sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

# Change to non-root privilege.
USER appuser

# install powerlevel10k
RUN git clone https://github.com/romkatv/powerlevel10k.git ~/.oh-my-zsh/custom/themes/powerlevel10k

RUN cd $HOME && curl -fsSLO https://raw.githubusercontent.com/romkatv/dotfiles-public/master/.purepower

# zsh configuration
ADD .zshrc $HOME

# Set the working directory.
WORKDIR /home/appuser/code/

# Expose port 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "chatgpt.wsgi"]
