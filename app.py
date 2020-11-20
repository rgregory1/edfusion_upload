import paramiko
from paramiko import sftp_client
import time
import credentials
from gr_prog_proc import process_gradeprog

# setup connection


def grab_file(file_name):

    # Get files from RaspberryPi

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(
        hostname=credentials.pi_host,
        username=credentials.pi_user,
        password=credentials.pi_pass,
        port=22,
    )
    sftp_client = ssh.open_sftp()

    sftp_client.get("/public/" + file_name, "incoming_files/" + file_name)

    sftp_client.close()
    ssh.close()


grab_file("03_5_PS_GradeProg.csv")

process_gradeprog()


# Put files to edfusion
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(
    hostname=credentials.ed_host,
    username=credentials.ed_user,
    password=credentials.ed_pass,
    look_for_keys=False,
)
sftp_client = ssh.open_sftp()


sftp_client.put("outgoing_files/03_5_PS_GradeProg.csv", "03_5_PS_GradeProg.csv")

sftp_client.close()
ssh.close()
