import docker
import time
client = docker.from_env()

for net in client.networks.list():
    if net.name == "se443_test_net":
        print("Network ID: ", net.id)
        print("Network Name: ", net.name)
        print("Network Creation Date: ", net.attrs['Created'])
        
#Subscriber                            
client.services.create("efrecon/mqtt-client", name="Subscriber",  restart_policy=docker.types.RestartPolicy(
        condition="any"), networks=["se443_test_net"], 
                       command='sub -h host.docker.internal -t Alfaisal_Uni -v').scale(3)
print(client.services.list()[0].id)
print(client.services.list()[0].name)
print(client.services.list()[0].attrs['CreatedAt'])
print(client.services.list()[0].attrs['Spec']['Mode']['Replicated']['Replicas'])

#Publisher
client.services.create("efrecon/mqtt-client", name="Publisher",  restart_policy=docker.types.RestartPolicy(
        condition="any"), networks=["se443_test_net"], 
                       command='pub -h host.docker.internal -t Alfaisal_Uni -m "<201394 - hissah - binsaidan>"').scale(3)
print(client.services.list()[0].id)
print(client.services.list()[0].name)
print(client.services.list()[0].attrs['CreatedAt'])
print(client.services.list()[0].attrs['Spec']['Mode']['Replicated']['Replicas'])

print("delay for 5 mins :)")
time.sleep(300)

print("\nRemoving Services...")

# Removing Publisher Service
print("Removing Publisher...", end="")
client.services.get("Publisher").remove()

# Removing Subcriber Service
print("Removing Subscriber...", end="")
client.services.get("Subscriber").remove()


# Removing Network
print("Removing Network...", end="")
client.networks.get("se443_test_net").remove()

# Removing Swarm
print("Removing Swarm...", end="")
client.swarm.leave(force=True)

