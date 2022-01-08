# vim: noexpandtab

LANGUAGE	?= french
COLOR		?= green

SRC_DIR 	:= .
TARGET_DIR	:= target
CONFIG_DIR	:= lang

SCRIPT 		:= script/generate.py

HEADER := $(SRC_DIR)/header.html
NAVBAR := $(SRC_DIR)/navbar.html
FOOTER := $(SRC_DIR)/footer.html

JSFOLDER 	:= js
JSTARGET	:= $(TARGET_DIR)/$(JSFOLDER)

CSSFOLDER	:= css
CSSTARGET	:= $(TARGET_DIR)/$(CSSFOLDER)

IMAGEFOLDER	:= images
IMAGETARGET	:= $(TARGET_DIR)/$(IMAGEFOLDER)

CONFIGFOLDER	:= $(CONFIG_DIR)
CONFIGTARGET	:= $(TARGET_DIR)/$(CONFIGFOLDER)

PRIVATEFOLDER	:= private
PRIVATETARGET	:= $(TARGET_DIR)/$(PRIVATEFOLDER)

.PHONY: all clean $(TARGET_DIR)

all: $(TARGET_DIR)/index.html $(TARGET_DIR)/publications.html $(TARGET_DIR)/teaching.html $(TARGET_DIR)/personal.html $(TARGET_DIR)/soutenance.html $(JSTARGET) $(CSSTARGET) $(IMAGETARGET) $(CONFIGTARGET) $(PRIVATETARGET)#$(TARGET_DIR)/portfolio.pdf

$(TARGET_DIR)/soutenance.html: $(SRC_DIR)/soutenance.html
	@cp $< $@

$(TARGET_DIR)/porfolio.pdf: $(SRC_DIR)/portfolio.pdf
	@ln -s $@ $<

$(TARGET_DIR)/%.html: $(HEADER) $(NAVBAR) $(FOOTER) $(TARGET_DIR) %.html
	@cat $(HEADER) 	> 	$@
	@cat $(NAVBAR) 	>> 	$@
	@cat $*.html 	>> 	$@
	@cat $(FOOTER) 	>> 	$@
	@python $(SCRIPT) $@ $@ $(CONFIG_DIR) --language $(LANGUAGE) --color $(COLOR)

$(TARGET_DIR):
	@mkdir -p $@

$(JSTARGET): $(SRC_DIR)/$(JSFOLDER)
	@rm -rf $@
	@cp -r $< $@

$(CSSTARGET): $(SRC_DIR)/$(CSSFOLDER)
	@rm -rf $@
	@cp -r $< $@

$(IMAGETARGET): $(SRC_DIR)/$(IMAGEFOLDER)
	@rm -rf $@
	@cp -r $< $@

$(CONFIGTARGET): $(SRC_DIR)/$(CONFIGFOLDER)
	@rm -rf $@
	@cp -r $< $@

$(PRIVATETARGET): $(SRC_DIR)/$(PRIVATEFOLDER)
	@rm -rf $@
	@cp -r $< $@

clean:
	@rm -rf $(TARGET_DIR)
