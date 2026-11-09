# FIXME: before you push into master...
RUNTIMEDIR=/usr/bin/../include/omc/c/
#COPY_RUNTIMEFILES=$(FMI_ME_OBJS:%= && (OMCFILE=% && cp $(RUNTIMEDIR)/$$OMCFILE.c $$OMCFILE.c))

fmu:
	rm -f 475.fmutmp/sources/roomM370_init.xml
	cp -a "/usr/bin/../share/omc/runtime/c/fmi/buildproject/"* 475.fmutmp/sources
	cp -a roomM370_FMU.libs 475.fmutmp/sources/

