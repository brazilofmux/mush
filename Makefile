RAGEL  ?= ragel
CC     ?= cc
CFLAGS ?= -O2

mdfix: mdfix.c
	$(CC) $(CFLAGS) -o $@ $<

mdfix.c: mdfix.rl
	$(RAGEL) -G2 $< -o $@

clean:
	rm -f mdfix mdfix.c

.PHONY: clean
