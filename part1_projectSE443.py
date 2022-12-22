import docker
import time
client = docker.from_env()
#part 1
client.swarm.leave(force = True)
client.swarm.init()

#Part B
print("this is Part B")
#print ID
print("Swarm ID: ", client.swarm.attrs['ID'])
#print Name
print("Swarm Name: ", client.swarm.attrs['Spec']['Name'])
#print Creation Date
print("Swarm Creation Date: ", client.swarm.attrs['CreatedAt'])


#part C 
print("this is part C")
client.networks.create("se443_test_net", driver = "overlay", scope ="global", 
                       
#part D
ipam = docker.types.IPAMConfig(pool_configs = [docker.types.IPAMPool(subnet = "10.10.10.0/24")]))
for net in client.networks.list():
    if net.name == "se443_test_net":
        print("Network ID: ", net.id)
        print("Network Name: ", net.name)
        print("Network Creation Date: ", net.attrs['Created'])
print("this is part D")

#part E
print("this is part E")
client.services.create("eclipse-mosquitto",name = "broker", restart_policy = docker.types.RestartPolicy(condition = "any")).scale(3) #restart "any" = always 
print(client.services.list()[0].id)
print(client.services.list()[0].name)
print(client.services.list()[0].attrs['CreatedAt'])
print(client.services.list()[0].attrs['Spec']['Mode']['Replicated']['Replicas'])



print("delay for 5 mins :)")
time.sleep(300)

# Removing Broker Service
print("\nRemoving Broker service")
client.services.get("broker").remove()
print("Broker removed")