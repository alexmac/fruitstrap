IOS_CC = clang

all: demo.app fruitstrap

demo.app: demo Info.plist
	mkdir -p demo.app
	cp demo demo.app/
	cp Info.plist ResourceRules.plist demo.app/
	codesign -f -s "iPhone Developer" --entitlements Entitlements.plist demo.app

demo: demo.c
	$(IOS_CC) -arch armv7 -isysroot /Applications/Xcode.app/Contents//Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS7.0.sdk -framework CoreFoundation -o demo demo.c

fruitstrap: fruitstrap.c
	clang -g -o fruitstrap -framework CoreFoundation -framework MobileDevice -F/System/Library/PrivateFrameworks fruitstrap.c

install: all
	./fruitstrap install --bundle=demo.app

debug: all
	./fruitstrap install --bundle=demo.app --debug

clean:
	rm -rf *.app demo fruitstrap
