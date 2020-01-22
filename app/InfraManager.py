import InfraBot
from InfraModule import InfraModule
from InfraManager_DB import db
import Database
import re

class InfraManager(InfraModule):
    def __init__(self, options=None):
        self.num = 0
        self.workspaces = {}
        super().__init__("infra", None)
        queries = Database.Status.query.all()

        for workspace in queries:
            dbWorkspace = Database.Workspaces.query.filter_by(id = workspace.workspace).first()
            if dbWorkspace is None:
                print("Workspace does not exist in database")
            else:
                self.workspaces[dbWorkspace.team_id] = workspace.workspace

    def api_entry(self, message, channel, user, team_id):
        if not team_id in self.workspaces:
            if not self.add_workspace_id(team_id):
                print("Workspace does not exist")
                return "Workspace " + team_id + " does not exist"
        #curStatus = Database.Status.query.filter_by(workspace = self.workspaces[team_id]).first()
        """ if curStatus is None:
            # Create new status
            newStatus = Database.Status(self.workspaces[team_id], statusType.GREEN)
            Database.db.session.add(newStatus)
            Database.db.session.commit()
            curStatus = newStatus """

        if message is "":
            self.send_error(None, channel, user, team_id)
            return "Status returned"
        
        # dns
        # dhcp
        # register
        # list
            # dns
            # dhcp
        # accept
            # dns
            # dhcp
        # decline
            # dns
            # dhcp

        if message.startswith("dns "):
            remainder = message[len("dns "):]
            ipcheck = re.search("^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$", remainder)
            if(not ipcheck):
                self.send_error("Invalid IP address", channel, user, team_id)
                return "Invalid IP Address"
            self.add_request("DNS", team_id, remainder)
            # if remainder.startswith("YELLOW") and curStatus.status == statusType.GREEN:
            #     #curStatus.status = statusType.YELLOW
            #     #InfraBot.notifyAdmins(InfraBot.getUserName(user, team_id) + " set status to YELLOW", team_id)
            # else:
            #     if not InfraBot.checkPermission(user, "admin", team_id):
            #         InfraBot.sendHelp("Access Denied", channel, user, team_id)
            #         return "Access Denied"
                
            #     if remainder == "GREEN":
            #         curStatus.status = statusType.GREEN
            #     elif remainder == "ORANGE":
            #         curStatus.status = statusType.ORANGE
            #     elif remainder == "PINK":
            #         curStatus.status = statusType.PINK
            #     elif remainder == "RED":
            #         curStatus.status = statusType.RED
            #     else:
            #         InfraBot.sendHelp("Invalid status.", channel, user, team_id)
            #         return "Invalid status selected"

            #     InfraBot.notifyAdmins(InfraBot.getUserName(user, team_id) + " set status set to " + curStatus.status.name, team_id)

            # if InfraBot.checkDM(channel, team_id):
            #     InfraBot.sendMessage("Status: " + curStatus.status.name, channel, team_id)
            # else:
            #     InfraBot.sendEphemeral("Status: " + curStatus.status.name, channel, user, team_id)
            
            # Database.db.session.commit()
            return InfraBot.getUserName(user, team_id) + " set status to " + curStatus.status.name
        elif message.startswith("dhcp "):
            return "asdf"
        elif message.startswith("register "):
            return "asdf"
        elif message.startswith("list "):
            remainder = message[len("list "):].upper()
            if remainder.startswith("DNS"):
                return "asdf"
            elif remainder.startswith()"DHCP"):
                return "asdf"
        elif message.startswith("accept "):
            remainder = message[len("accept "):].upper()
            if remainder.startswith("DNS"):
                return "asdf"
            elif remainder.startswith()"DHCP"):
                return "asdf"
        elif message.startswith("decline "):
            remainder = message[len("decline "):].upper()
            if remainder.startswith("DNS"):
                return "asdf"
            elif remainder.startswith()"DHCP"):
                return "asdf"
        elif message.startswith("help"):
            self.send_error(None, channel, user, team_id)
        else:
            self.send_error("Invalid command", channel, user, team_id)

    def agent_endpoint(self, agent_type, team_id):
        return "Function not yet implemented"

    def add_workspace_id(self, team_id):
        dbWorkspace = Database.Workspaces.query.filter_by(team_id = team_id).first()
        if dbWorkspace is None:
            print("Workspace does not exist in database")
            return False
        else:
            self.workspaces[team_id] = dbWorkspace.id
            return True
    
    def add_request(self, request_type, team_id, request_data):
        if request_data = "DNS":
            return "asdf"
        elif request_data = "DHCP":
            return "asdf"
        return "ERROR"

    def send_error(self, message, channel, user, team_id):
        messageString = ""
        if not message is None:
            messageString += message +"\n\n"
        messageString += "Status Help:\n"
        messageString += "\t!request dns <ip address> - adds a request to delegate the <username>.playground.ksucdc.org DNS zone to the given ip address\n"
        messageString += "\t\t- CDC username must be registered, do !request register <CDC username> to do this\n"
        messageString += "\t!request dhcp <mac address> - adds a request to get a static dhcp reservation for the given ip address\n"
        messageString += "\t!request status - Lists the status of all of your requests"
        messageString += "\t!request register <CDC username> - Request to register your CDC username to your Slack username"
        if InfraBot.checkPermission(user, "admin", team_id):
            messageString += "\t!request list <dns/dhcp/register> - lists all requests of the given type (requires admin privileges)\n"
            messageString += "\t!request accept <dns/dhcp/register> <request id> - accepts a request (requires admin privileges)\n"
            messageString += "\t!request decline <dns/dhcp/register> <request id> - declines a dns, dhcp, or register request (requires admin privileges)\n"


        messageString += "\t!request help - Prints this help prompt\n"

        InfraBot.sendEphemeral(messageString, channel, user, team_id)
