# vim: noexpandtab

LANGUAGE	?= english
COLOR		?= green

SRC_DIR 	:= .
HTML_DIR	:= html
CONFIG_DIR	:= lang
DOCUMENT_DIR := doc
TARGET_DIR	:= htdocs

DIST 		:= yulpa
DIST_PATH 	:= /datas/yulpa172811/sites/ferres.me

SCRIPT 		:= script/generate.py

HEADER := $(HTML_DIR)/header.html
NAVBAR := $(HTML_DIR)/navbar.html
FOOTER := $(HTML_DIR)/footer.html

JSFOLDER 	:= js
JSTARGET	:= $(TARGET_DIR)/$(JSFOLDER)

CSSFOLDER	:= css
CSSTARGET	:= $(TARGET_DIR)/$(CSSFOLDER)
CSSSRC		:= $(wildcard $(SRC_DIR)/$(CSSFOLDER)/*.css)

IMAGEFOLDER	:= images
IMAGETARGET	:= $(TARGET_DIR)/$(IMAGEFOLDER)

CONFIGFOLDER	:= $(CONFIG_DIR)
CONFIGTARGET	:= $(TARGET_DIR)/$(CONFIGFOLDER)
CONFIGSOURCES 	:= $(wildcard $(CONFIG_DIR)/*.json)

.PHONY: all clean $(TARGET_DIR) required www

all: clean required $(JSTARGET) $(CSSTARGET) $(IMAGETARGET) $(CONFIGTARGET) documents 

required: $(TARGET_DIR)/index.html \
	$(TARGET_DIR)/curriculum.html \
	$(TARGET_DIR)/research.html \
	$(TARGET_DIR)/software.html \
	$(TARGET_DIR)/teaching.html \
	$(TARGET_DIR)/personal.html \
	$(TARGET_DIR)/phd.html

documents: $(TARGET_DIR)/$(DOCUMENT_DIR)

$(TARGET_DIR)/$(DOCUMENT_DIR): $(DOCUMENT_DIR)
	@cp -r $< $(TARGET_DIR)

$(TARGET_DIR)/phd.html: $(HTML_DIR)/phd.html
	@cp $< $@

$(TARGET_DIR)/%.html: $(HEADER) $(NAVBAR) $(FOOTER) $(TARGET_DIR) $(HTML_DIR)/%.html
	@cat $(HEADER) 				> 	$@
	@cat $(NAVBAR) 				>> 	$@
	@cat $(HTML_DIR)/$*.html 	>> 	$@
	@cat $(FOOTER) 				>> 	$@
	@python $(SCRIPT) $@ $@ $(CONFIG_DIR) --language $(LANGUAGE) --color $(COLOR)

$(TARGET_DIR):
	@mkdir -p $@

$(JSTARGET): $(SRC_DIR)/$(JSFOLDER)
	@rm -rf $@
	@cp -r $< $@
	@sed -i s/"defaultLang = 'english'"/"defaultLang = '$(LANGUAGE)'"/g $(JSTARGET)/custom.js

$(CSSTARGET): $(SRC_DIR)/$(CSSFOLDER) $(CSSSRC)
	@rm -rf $@
	@cp -r $< $@

$(IMAGETARGET): $(SRC_DIR)/$(IMAGEFOLDER)
	@rm -rf $@
	@cp -r $< $@

$(CONFIGTARGET): $(SRC_DIR)/$(CONFIGFOLDER) $(CONFIGSOURCES)
	@rm -rf $@
	@cp -r $< $@

clean:
	@rm -rf $(TARGET_DIR)

www: all
	@scp -r $(TARGET_DIR) $(DIST):$(DIST_PATH)
