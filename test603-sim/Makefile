PRODUCTS = \
  example

WARNINGS = \
  -std=c++14 \
  -pedantic \
  -Wall \
  -Wextra \
  -Wconversion \
  -Wsign-conversion \
  -Wshadow \
  -Wno-c99-extensions

OPTFLAGS = \
  -O2

DBGFLAGS = \
  -g \
  -fsanitize=address

CXXFLAGS = \
  $(WARNINGS) \
  $(OPTFLAGS) \
  $(DBGFLAGS) \
  $(EXTRA_CXXFLAGS)

ARTIFACTS = \
  $(PRODUCTS) \
  *.dSYM

.PHONY: all clean
.SUFFIXES: .cc

all: $(PRODUCTS)
	@:

clean:
	rm -rf $(ARTIFACTS)

.cc:
	$(CXX) $(CXXFLAGS) $(LDFLAGS) -o $@ $<

example: sim.hpp
