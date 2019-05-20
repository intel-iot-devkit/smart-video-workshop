## Lab setup
Set the folder to execute labs in the workshop github.

### Download workshop content and set directory path
#### 1. Create the workshop directory

	sudo mkdir -p /opt/intel/workshop/
	
#### 2. Change ownership of the workshop directory to the current user 

> **Note:** *replace the usernames below with your user account name*
		
	sudo chown username.username -R /opt/intel/workshop/

#### 3. Navigate to the new directory

	cd /opt/intel/workshop/

#### 4. Download and clone the workshop content to the current directory (/opt/intel/workshop/smart-video-workshop).

	git clone https://github.com/intel-iot-devkit/smart-video-workshop.git
	
If you get a fatal message, "fatal: destination path 'smart-video-workshop' already exists and is not an empty directory.
",

	cd /opt/intel/workshop/smart-video-workshop/
	git pull

#### 5. Set short path for the workshop directory

	export SV=/opt/intel/workshop/smart-video-workshop/
