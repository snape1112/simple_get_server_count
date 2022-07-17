import math

# server resource
template_server = {
    "cpu": 3.8,
    "ram": 16,
    "harddisk": 100
}

# apps resource
template_apps = [
    {"cpu": 2.5, "ram": 11,"harddisk": 15},
    {"cpu": 1.5, "ram": 2,"harddisk": 95},
    {"cpu": 1.5, "ram": 2,"harddisk": 45},
    {"cpu": 0.5, "ram": 7,"harddisk": 55},
    {"cpu": 1.3, "ram": 4,"harddisk": 32},
    {"cpu": 1.8, "ram": 6,"harddisk": 29},
    {"cpu": 2, "ram": 2,"harddisk": 65},
    {"cpu": 0.5, "ram": 5,"harddisk": 15}
]

################################# How to calculate? #################################
# Step 1:
#   Get the minimum number of servers
# Step 2:
#   Check the number and increase if not
# How to check the number of servers:
#   From the first app, deploy it into different servers in order.
#   But avoid same deployments in the meaning like [['App1'], ['App2', 'App3'], ['App4', 'App5']] = [['App4', 'App5'], ['App3', 'App2'], ['App1']]

# number of servers
serverCount = 0
# resource status when apps are deployed
serverResource = []
# which apps are deployed into the server
serverApp = []
    
# add values of two resource
def addResource (first, second) :
    for key in first :
        first[key] = first[key] + second[key]

# sub values of two ability
def subResource (first, second) :
    for key in first :
        first[key] = first[key] - second[key]

# check resource overflow when the app is put
def canDeployApp (app, server) :
    temp = serverResource[server].copy()
    addResource(temp, template_apps[app])
    for field in temp :
        if temp[field] > template_server[field] :
            return False
    return True

# put app into server
def deployAppTo (app, server) :
    addResource(serverResource[server], template_apps[app])
    serverApp[server].append("App" + str(app + 1))

# take last appended app from server
def popAppFrom (app, server) :
    subResource(serverResource[server], template_apps[app])
    serverApp[server].pop()

# check if server count is enough
def isValid (app, max_server):
    if app == len(template_apps) :
        return True
    for server in range(max_server + 2) :
        if server == serverCount :
            break
        if canDeployApp(app, server) :
            deployAppTo(app, server)
            if isValid(app + 1, max(server, max_server)) :
                return True
            popAppFrom(app, server)
        server += 1
    return False

# sum of apps resources
total = {"cpu": 0, "ram": 0, "harddisk": 0}
for app in template_apps :
    addResource(total, app)
# minimum server count
serverCount = 0
for field in template_server :
    serverCount = max(serverCount, math.ceil(total[field] / template_server[field]))
# try server count by increasing
deployed = False
while serverCount <= len(template_apps) :
    # init server resource
    serverResource = []
    serverApp = []
    for i in range(serverCount) :
        serverResource.append({"cpu": 0, "ram": 0, "harddisk": 0})
        serverApp.append([])
    # put first app to first server
    if canDeployApp(0, 0) == False :
        break
    deployAppTo(0, 0)
    # check server count
    if isValid(1, 0) :
        print("Number of Servers:", serverCount)
        for i in range(len(serverApp)) :
            print("Server", i + 1, serverApp[i])
        deployed = True
        break
    serverCount += 1
if deployed == False :
    print("Invalid")
