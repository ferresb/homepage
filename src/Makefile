# vim: noexpandtab

LANGUAGE	?= french
COLOR		?= green

SCRIPT 		:= script/generate.py

SRC_DIR 	:= .
TMP_DIR 	:= tmp
TARGET_DIR	:= target
CONFIG_DIR	:= ../lang

HEADER := $(SRC_DIR)/header.html
NAVBAR := $(SRC_DIR)/navbar.html
FOOTER := $(SRC_DIR)/footer.html

.PHONY: all clean realclean

all: $(TARGET_DIR)/index.html

$(TARGET_DIR)/index.html: $(TMP_DIR)/index.html $(TARGET_DIR)
	@cp $< $@

$(TMP_DIR)/index.html: $(HEADER) $(NAVBAR) $(FOOTER) $(TMP_DIR) index.html
	@cat $(HEADER) 	> 	$@
	@cat $(NAVBAR) 	>> 	$@
	@cat index.html >> 	$@
	@cat $(FOOTER) 	>> 	$@
	@python $(SCRIPT) $@ $@ $(CONFIG_DIR) --language $(LANGUAGE) --color $(COLOR)

$(TMP_DIR):
	@mkdir -p $@

$(TARGET_DIR):
	@mkdir -p $@

clean:
	@rm -rf $(TMP_DIR)

realclean: clean
	@rm -rf $(TARGET_DIR)
