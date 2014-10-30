STABMAN_DIR := stabmanager
SMM_DIR := smm
USRAPP_DIR := usrapp

STABMAN := stabman
SMM := smm_prof
USRAPP := client

compile:	
	$(MAKE) -C $(STABMAN_DIR)
	$(MAKE) -C $(SMM_DIR)
	$(MAKE) -C $(USRAPP_DIR)
	
install:
	insmod $(STABMAN_DIR)/$(STABMAN).ko
	insmod $(SMM_DIR)/$(SMM).ko
	$(USRAPP_DIR)/$(USRAPP) $(SYSMAP)
	
uninstall:
	rmmod $(SMM)
	rmmod $(STABMAN)
	
clean:
	$(MAKE) -C $(STABMAN_DIR) clean
	$(MAKE) -C $(SMM_DIR) clean
	$(MAKE) -C $(USRAPP_DIR) clean