include config.mk

SOURCES	= wtime.c
BIN = wtime wtlog wthours
MAN1 = wtime.1

all: wtime

wtime:	wtime.c
		$(CC) $(CFLAGS) $< -o $@

clean:
		rm -f wtime *.o

install: all
		${MKDIR} -p ${PREFIX}/bin
		${CP} ${BIN} ${PREFIX}/bin
		for i in ${BIN}; do \
			chmod 755 ${PREFIX}/bin/`basename $$i`; \
		done
		${MKDIR} -p ${PREFIX}/man/man1
		${CP} ${MAN1} ${PREFIX}/man/man1
		for i in ${MAN1}; do \
			chmod 444 ${PREFIX}/man/man1/`basename $$i`; \
		done

uninstall:
		for i in ${BIN}; do \
			${RM} -f ${PREFIX}/bin/`basename $$i`; \
		done
		for i in ${MAN1}; do \
			${RM} -f ${PREFIX}/man/man1/`basename $$i`; \
		done
