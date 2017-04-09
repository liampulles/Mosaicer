all:
	g++ mosaicer.cpp EasyBMP/EasyBMP.cpp -std=c++11 -o mosaicer

clean:
	rm mosaicer
