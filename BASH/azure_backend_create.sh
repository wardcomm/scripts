#!/bin/bash


# STORAGE_ACCOUNT_NAME=tfstate$RANDOM
# CONTAINER_NAME=tfstate
# LOCATION=eastus


# SUBSCRIPTION=27547eca-06d8-41cb-a10f-c0c5028e5313
# TENANT=a7ecaa8d-4880-4bcd-8c42-7d53d21b35bb
# az login -u ncah61@ccbcc.com --$SUBSCRIPTION 
# ==================================================================
STORAGE_ACCOUNT_NAME=tfstate$RANDOM
CONTAINER_NAME=tfstate
RESOURCE_GROUP_NAME="RG-$ENV-$ITEM"
ITEM="tfstate"
ENV1="CORE-01"
ENV2="NON-PROD-01"
ENV3="NON-PROD-02"
ENV4="EXT-DMZ-01"
ENV5="PROD-01"
ENV6="PROD-02"
ENV7="SANDBOX-01"

LOC1="eastus"
LOC2="eastus"
LOC3="eastus2"
LOC4="eastus"
LOC5="eastus2"
LOC6="eastus2"
LOC7="eastus"

firstRG="RG-$ENV1-$ITEM"
secondRG="RG-$ENV2-$ITEM"
thirdRG="RG-$ENV3-$ITEM"
forthRG="RG-$ENV4-$ITEM"
FifthRG="RG-$ENV5-$ITEM"
sixthRG="RG-$ENV6-$ITEM"
seventhRG="RG-$ENV7-$ITEM"

firstSub="27547eca-06d8-41cb-a10f-c0c5028e5313"
secondSub="687f831f-9ab5-4b4b-8c9e-6dafd1dddd5f"
thirdSub="a13a4bc1-3b9c-4a72-af5b-7f13fb7d1309"
forthSub="26556710-8038-4b86-adb0-643df6505c5d"
fifthSub="2964c3e1-f7e8-4327-b7f8-087b55cb75ce"
sixthSub="3fc54023-25d2-45bc-9484-9d4a71f209a2"
seventhSub="8afd51c9-71f4-4465-a252-841e10fc9c08"

az account set --subscription $firstSub
az group create --name $firstRG --location $LOC1
# Create storage account
az storage account create --resource-group $RESOURCE_GROUP_NAME --name $STORAGE_ACCOUNT_NAME --sku Standard_LRS --encryption-services blob
# Get storage account key
ACCOUNT_KEY=$(az storage account keys list --resource-group $firstRG --account-name $STORAGE_ACCOUNT_NAME --query [0].value -o tsv)
# Create blob container
az storage container create --name $CONTAINER_NAME --account-name $STORAGE_ACCOUNT_NAME --account-key $ACCOUNT_KEY
echo "storage_account_name: $STORAGE_ACCOUNT_NAME"
echo "container_name: $CONTAINER_NAME"
echo "access_key: $ACCOUNT_KEY"

az account set --subscription $secondSub
az group create --name $secondRG --location $LOC2
# Create storage account
az storage account create --resource-group $RESOURCE_GROUP_NAME --name $STORAGE_ACCOUNT_NAME --sku Standard_LRS --encryption-services blob
# Get storage account key
ACCOUNT_KEY=$(az storage account keys list --resource-group $secondRG --account-name $STORAGE_ACCOUNT_NAME --query [0].value -o tsv)
# Create blob container
az storage container create --name $CONTAINER_NAME --account-name $STORAGE_ACCOUNT_NAME --account-key $ACCOUNT_KEY
echo "storage_account_name: $STORAGE_ACCOUNT_NAME"
echo "container_name: $CONTAINER_NAME"
echo "access_key: $ACCOUNT_KEY"

az account set --subscription $thirdSub
az group create --name $thirdRG --location $LOC3
# Create storage account
az storage account create --resource-group $RESOURCE_GROUP_NAME --name $STORAGE_ACCOUNT_NAME --sku Standard_LRS --encryption-services blob
# Get storage account key
ACCOUNT_KEY=$(az storage account keys list --resource-group $thirdRG --account-name $STORAGE_ACCOUNT_NAME --query [0].value -o tsv)
# Create blob container
az storage container create --name $CONTAINER_NAME --account-name $STORAGE_ACCOUNT_NAME --account-key $ACCOUNT_KEY
echo "storage_account_name: $STORAGE_ACCOUNT_NAME"
echo "container_name: $CONTAINER_NAME"
echo "access_key: $ACCOUNT_KEY"

az account set --subscription $forthSub
az group create --name $forthRG --location $LOC4
# Create storage account
az storage account create --resource-group $RESOURCE_GROUP_NAME --name $STORAGE_ACCOUNT_NAME --sku Standard_LRS --encryption-services blob
# Get storage account key
ACCOUNT_KEY=$(az storage account keys list --resource-group $forthRG --account-name $STORAGE_ACCOUNT_NAME --query [0].value -o tsv)
# Create blob container
az storage container create --name $CONTAINER_NAME --account-name $STORAGE_ACCOUNT_NAME --account-key $ACCOUNT_KEY
echo "storage_account_name: $STORAGE_ACCOUNT_NAME"
echo "container_name: $CONTAINER_NAME"
echo "access_key: $ACCOUNT_KEY"

az account set --subscription $fifthSub
az group create --name $FifthRG --location $LOC5
# Create storage account
az storage account create --resource-group $RESOURCE_GROUP_NAME --name $STORAGE_ACCOUNT_NAME --sku Standard_LRS --encryption-services blob
# Get storage account key
ACCOUNT_KEY=$(az storage account keys list --resource-group $fifthRG --account-name $STORAGE_ACCOUNT_NAME --query [0].value -o tsv)
# Create blob container
az storage container create --name $CONTAINER_NAME --account-name $STORAGE_ACCOUNT_NAME --account-key $ACCOUNT_KEY
echo "storage_account_name: $STORAGE_ACCOUNT_NAME"
echo "container_name: $CONTAINER_NAME"
echo "access_key: $ACCOUNT_KEY"

az account set --subscription $sixthSub
az group create --name $sixthRG --location $LOC6
# Create storage account
az storage account create --resource-group $RESOURCE_GROUP_NAME --name $STORAGE_ACCOUNT_NAME --sku Standard_LRS --encryption-services blob
# Get storage account key
ACCOUNT_KEY=$(az storage account keys list --resource-group $sixthRG --account-name $STORAGE_ACCOUNT_NAME --query [0].value -o tsv)
# Create blob container
az storage container create --name $CONTAINER_NAME --account-name $STORAGE_ACCOUNT_NAME --account-key $ACCOUNT_KEY
echo "storage_account_name: $STORAGE_ACCOUNT_NAME"
echo "container_name: $CONTAINER_NAME"
echo "access_key: $ACCOUNT_KEY"


az account set --subscription $seventhSub
az group create --name $seventhRG --location $LOC7
# Create storage account
az storage account create --resource-group $RESOURCE_GROUP_NAME --name $STORAGE_ACCOUNT_NAME --sku Standard_LRS --encryption-services blob
# Get storage account key
ACCOUNT_KEY=$(az storage account keys list --resource-group $sevethRG --account-name $STORAGE_ACCOUNT_NAME --query [0].value -o tsv)
# Create blob container
az storage container create --name $CONTAINER_NAME --account-name $STORAGE_ACCOUNT_NAME --account-key $ACCOUNT_KEY
echo "storage_account_name: $STORAGE_ACCOUNT_NAME"
echo "container_name: $CONTAINER_NAME"
echo "access_key: $ACCOUNT_KEY"

# az group deployment create \
#   --name ExampleDeployment \
#   --resource-group $firstRG \
#   --template-uri https://raw.githubusercontent.com/Azure/azure-docs-json-samples/master/azure-resource-manager/crosssubscription.json \
#   --parameters storagePrefix=storage secondResourceGroup=$secondRG secondStorageLocation=eastus secondSubscriptionID=$secondSub

# ==================================================================

# # Create resource group
# az group create --name $RESOURCE_GROUP_NAME --location $LOCATION

# # Create storage account
# az storage account create --resource-group $RESOURCE_GROUP_NAME --name $STORAGE_ACCOUNT_NAME --sku Standard_LRS --encryption-services blob
# # Get storage account key
# ACCOUNT_KEY=$(az storage account keys list --resource-group $RESOURCE_GROUP_NAME --account-name $STORAGE_ACCOUNT_NAME --query [0].value -o tsv)
# # Create blob container
# az storage container create --name $CONTAINER_NAME --account-name $STORAGE_ACCOUNT_NAME --account-key $ACCOUNT_KEY
# echo "storage_account_name: $STORAGE_ACCOUNT_NAME"
# echo "container_name: $CONTAINER_NAME"
# echo "access_key: $ACCOUNT_KEY"