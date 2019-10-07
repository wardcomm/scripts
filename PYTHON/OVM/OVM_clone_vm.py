import ovmclient
user = "p2906297"
password = "THem5dax"
server = "https://ovmdmgr04:7002/ovm/core/wsapi/rest"
client = ovmclient.Client( 'server', 'user', 'password')

# Make sure the manager is running
client.managers.wait_for_manager_state()

pool_id = client.server_pools.get_id_by_name('pool1')

# Get an existing VM or a VM template
vm_id = client.vms.get_id_by_name('vm1')

# Set to True to create a VM template, False for a regular VM
create_template = False

# Clone the VM
job = client.jobs.wait_for_job(
    client.vms.clone(vm_id, pool_id, create_template=create_template))
new_vm_id = job['resultId']