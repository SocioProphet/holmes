.PHONY: build test validate dist release-dry-run clean

BIN := holmes
DIST_DIR := dist
VERSION ?= 0.1.0-dev
COMMIT ?= $(shell git rev-parse --short HEAD 2>/dev/null || echo unknown)
DATE ?= $(shell date -u +%Y-%m-%dT%H:%M:%SZ)
GOOS ?= $(shell go env GOOS 2>/dev/null || uname -s | tr A-Z a-z)
GOARCH ?= $(shell go env GOARCH 2>/dev/null || uname -m)
DIST_NAME := $(BIN)_$(VERSION)_$(GOOS)_$(GOARCH)
LDFLAGS := -X main.version=$(VERSION) -X main.commit=$(COMMIT) -X main.date=$(DATE)

build:
	mkdir -p bin
	go build -ldflags "$(LDFLAGS)" -o bin/$(BIN) ./cmd/holmes

test:
	go test ./...

validate: build
	python3 tools/validate_holmes.py
	bin/$(BIN) --version
	bin/$(BIN) doctor
	bin/$(BIN) self-test
	bin/$(BIN) emit-evidence >/tmp/holmes-evidence.json
	bin/$(BIN) analyze examples/sample.txt >/tmp/holmes-analysis.json
	bin/$(BIN) search "truth and evidence" >/tmp/holmes-search.json
	bin/$(BIN) graph examples/sample.txt >/tmp/holmes-graph.json
	bin/$(BIN) govern examples/sample.txt >/tmp/holmes-govern.json

dist: validate
	mkdir -p $(DIST_DIR)
	cp bin/$(BIN) $(DIST_DIR)/$(DIST_NAME)
	(cd $(DIST_DIR) && sha256sum $(DIST_NAME) > $(DIST_NAME).sha256)

release-dry-run: dist
	@echo "release dry-run complete: $(DIST_DIR)/$(DIST_NAME)"

clean:
	rm -rf bin $(DIST_DIR)
