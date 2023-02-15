# vim: noexpandtab

LANGUAGE	?= english
COLOR		?= green

SRC_DIR 	:= .
HTML_DIR	:= html
TARGET_DIR	:= target
CONFIG_DIR	:= lang

SCRIPT 		:= script/generate.py

HEADER := $(HTML_DIR)/header.html
NAVBAR := $(HTML_DIR)/navbar.html
FOOTER := $(HTML_DIR)/footer.html

JSFOLDER 	:= js
JSTARGET	:= $(TARGET_DIR)/$(JSFOLDER)

CSSFOLDER	:= css
CSSTARGET	:= $(TARGET_DIR)/$(CSSFOLDER)

IMAGEFOLDER	:= images
IMAGETARGET	:= $(TARGET_DIR)/$(IMAGEFOLDER)

CONFIGFOLDER	:= $(CONFIG_DIR)
CONFIGTARGET	:= $(TARGET_DIR)/$(CONFIGFOLDER)

.PHONY: all clean $(TARGET_DIR) required

all: required $(JSTARGET) $(CSSTARGET) $(IMAGETARGET) $(CONFIGTARGET) documents 

required: $(TARGET_DIR)/index.html $(TARGET_DIR)/publications.html $(TARGET_DIR)/teaching.html $(TARGET_DIR)/personal.html $(TARGET_DIR)/soutenance.html

documents: $(TARGET_DIR)/portfolio.pdf $(TARGET_DIR)/slides.pdf $(TARGET_DIR)/CV_FerresBruno.pdf

$(TARGET_DIR)/soutenance.html: $(HTML_DIR)/soutenance.html
	@cp $< $@

$(TARGET_DIR)/portfolio.pdf: portfolio.pdf
	@cp --preserve=links $< $@

$(TARGET_DIR)/resume_francais.pdf: resume_francais.pdf
	@cp --preserve=links $< $@

$(TARGET_DIR)/slides.pdf: slides.pdf
	@cp --preserve=links $< $@

$(TARGET_DIR)/CV_FerresBruno.pdf: CV_FerresBruno.pdf
	@cp --preserve=links $< $@

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

$(CSSTARGET): $(SRC_DIR)/$(CSSFOLDER)
	@rm -rf $@
	@cp -r $< $@

$(IMAGETARGET): $(SRC_DIR)/$(IMAGEFOLDER)
	@rm -rf $@
	@cp -r $< $@

$(CONFIGTARGET): $(SRC_DIR)/$(CONFIGFOLDER)
	@rm -rf $@
	@cp -r $< $@

clean:
	@rm -rf $(TARGET_DIR)
