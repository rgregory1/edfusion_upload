import paramiko
from paramiko import sftp_client
import datetime
import credentials
from gr_prog_proc import process_gradeprog
from ps_att_proc import process_att

# get timestamp for log
temp_timestamp = str(datetime.datetime.now())
print(2 * "\n")
print(temp_timestamp)


# setup connection


def grab_files(file_list):

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

    files = sftp_client.listdir()
    print(files)

    for file_name in file_list:
        sftp_client.get("/public/" + file_name, "incoming_files/" + file_name)
        print(f"Retrieved {file_name} from remote")

    sftp_client.close()
    ssh.close()


grab_files(["03_7_PS_Att.csv"])


# process_gradeprog()
process_att()

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


sftp_client.put("outgoing_files/03_7_PS_Att.csv", "03_7_PS_Att.csv")
print("Put file on remote server")
sftp_client.close()
ssh.close()
