import ovmclient
from ovmclient import constants

client = ovmclient.Client(
    'https://ovmdmgr04:7002/ovm/core/wsapi/rest', 'p2906297', 'THem5dax')

# Make sure the manager is running
client.managers.wait_for_manager_state()

repo_id = client.repositories.get_id_by_name('repo1')
pool_id = client.server_pools.get_id_by_name('pool1')
network_id = client.networks.get_id_by_name('management')

# Create a virtual disk
disk_data = {
    'diskType': constants.DISK_TYPE_VIRTUAL_DISK,
    'size': 1024 * 1024 * 1024,
    'shareable': False,
    'name': 'dummy.img',
}

job = client.jobs.wait_for_job(
    client.repository_virtual_disks(repo_id).create(disk_data, sparse='true'))
disk_id = job['resultId']

# Create a VM
vm_data = {
    'name': 'vm1',
    'description': 'Blah',
    'vmDomainType': constants.VM_DOMAIN_TYPE_XEN_HVM_PV_DRIVERS,
    'repositoryId': repo_id,
    'serverPoolId': pool_id,
    'cpuCount': 4,
    'cpuCountLimit': 4,
    'hugePagesEnabled': False,
    'memory': 1024,
    'memoryLimit': 1024,
    'osType': 'Oracle Linux 7',
}

job = client.jobs.wait_for_job(client.vms.create(vm_data))
vm_id = job['resultId']

# Map the virtual disk
vm_disk_mapping_data = {
    'virtualDiskId': disk_id,
    'diskWriteMode': constants.DISK_WRITE_MODE_READ_WRITE,
    'emulatedBlockDevice': False,
    'storageElementId': None,
    'diskTarget': 0,
}

job = client.jobs.wait_for_job(
    client.vm_disk_mappings(vm_id).create(vm_disk_mapping_data))

# Add a vnic
vnic_data = {
    'networkId': network_id,
}

client.jobs.wait_for_job(client.vm_virtual_nics(vm_id).create(vnic_data))

# Retrieve the VM
vm = client.vms.get_by_id(vm_id)

# Update the VM, e.g. setting a new name
vm['name'] = 'vm2'
client.jobs.wait_for_job(client.vms.update(vm_id, vm))

# Start the VM
client.jobs.wait_for_job(client.vms.start(vm_id))

# Kill the VM
client.jobs.wait_for_job(client.vms.kill(vm_id))

# Delete the VM
client.jobs.wait_for_job(client.vms.delete(vm_id))

# Delete the virtual disk
client.jobs.wait_for_job(
    client.repository_virtual_disks(repo_id).delete(disk_id))