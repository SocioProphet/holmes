package main

import (
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"errors"
	"fmt"
	"os"
	"path/filepath"
	"strings"
)

var (
	version = "0.1.0-dev"
	commit  = "unknown"
	date    = "unknown"
)

type evidence struct {
	Tool      string         `json:"tool"`
	Version   string         `json:"version"`
	Commit    string         `json:"commit"`
	BuildDate string         `json:"buildDate"`
	Repo      string         `json:"repo"`
	Command   string         `json:"command"`
	Status    string         `json:"status"`
	Details   map[string]any `json:"details,omitempty"`
}

type analysisRecord struct {
	Tool        string   `json:"tool"`
	Version     string   `json:"version"`
	Status      string   `json:"status"`
	Path        string   `json:"path"`
	Bytes       int      `json:"bytes"`
	SHA256      string   `json:"sha256"`
	Lines       int      `json:"lines"`
	Words       int      `json:"words"`
	Components  []string `json:"components"`
	EvidenceRef string   `json:"evidenceRef"`
}

func usage() {
	fmt.Fprintf(os.Stderr, `holmes %s

Usage:
  holmes --version
  holmes doctor
  holmes self-test
  holmes emit-evidence
  holmes analyze <path>
  holmes search <query>
  holmes graph <path>
  holmes govern <path>

`, version)
}

func main() {
	if len(os.Args) == 1 {
		usage()
		os.Exit(2)
	}
	if os.Args[1] == "--version" || os.Args[1] == "version" {
		fmt.Printf("holmes %s commit=%s date=%s\n", version, commit, date)
		return
	}

	switch os.Args[1] {
	case "doctor":
		runDoctor()
	case "self-test":
		runSelfTest()
	case "emit-evidence":
		runEvidence("emit-evidence", "ok", map[string]any{"surface": "language-intelligence", "mode": "local"})
	case "analyze":
		requireArgs(os.Args, 3)
		runAnalyze(os.Args[2])
	case "search":
		requireArgs(os.Args, 3)
		runSearch(strings.Join(os.Args[2:], " "))
	case "graph":
		requireArgs(os.Args, 3)
		runGraph(os.Args[2])
	case "govern":
		requireArgs(os.Args, 3)
		runGovern(os.Args[2])
	default:
		usage()
		os.Exit(2)
	}
}

func requireArgs(args []string, n int) {
	if len(args) < n {
		usage()
		os.Exit(2)
	}
}

func runDoctor() {
	details := map[string]any{
		"components": []string{"sherlock-search", "221b", "mycroft-router", "moriarty-bench", "irene-shield", "the-canon", "deduction-engine"},
		"wired":      []string{},
		"pending":    []string{"sherlock-search", "221b", "mycroft-router", "moriarty-bench", "irene-shield", "the-canon", "deduction-engine"},
	}
	runEvidence("doctor", "not-yet-wired", details)
}

func runSelfTest() {
	if _, err := os.Stat("examples/holmes-surface.json"); err != nil {
		runEvidence("self-test", "failed", map[string]any{"error": err.Error()})
		os.Exit(1)
	}
	runEvidence("self-test", "ok", map[string]any{"example": "examples/holmes-surface.json"})
}

func runAnalyze(path string) {
	record, err := analyzeFile(path)
	if err != nil {
		printJSON(map[string]any{"status": "failed", "error": err.Error(), "path": path})
		os.Exit(1)
	}
	printJSON(record)
}

func runSearch(query string) {
	printJSON(map[string]any{
		"tool":       "holmes",
		"version":    version,
		"status":     "not-yet-wired",
		"query":      query,
		"engine":     "sherlock-search",
		"message":    "Sherlock Search binding is declared but runtime search is not wired in this CLI skeleton.",
		"evidenceId": stableID("search:" + query),
	})
}

func runGraph(path string) {
	record, err := analyzeFile(path)
	if err != nil {
		printJSON(map[string]any{"status": "failed", "error": err.Error(), "path": path})
		os.Exit(1)
	}
	printJSON(map[string]any{
		"tool":       "holmes",
		"version":    version,
		"status":     "not-yet-wired",
		"path":       record.Path,
		"sha256":     record.SHA256,
		"target":     "language.graph.v1/ToSemanticGraph",
		"message":    "Semantic graph conversion is declared but not wired in this CLI skeleton.",
		"evidenceId": stableID("graph:" + record.SHA256),
	})
}

func runGovern(path string) {
	record, err := analyzeFile(path)
	if err != nil {
		printJSON(map[string]any{"status": "failed", "error": err.Error(), "path": path})
		os.Exit(1)
	}
	printJSON(map[string]any{
		"tool":       "holmes",
		"version":    version,
		"status":     "not-yet-wired",
		"path":       record.Path,
		"sha256":     record.SHA256,
		"target":     "language.govern.v1/Evaluate",
		"message":    "Governance/eval binding is declared but not wired in this CLI skeleton.",
		"evidenceId": stableID("govern:" + record.SHA256),
	})
}

func analyzeFile(path string) (analysisRecord, error) {
	clean := filepath.Clean(path)
	bytes, err := os.ReadFile(clean)
	if err != nil {
		return analysisRecord{}, err
	}
	text := string(bytes)
	sum := sha256.Sum256(bytes)
	record := analysisRecord{
		Tool:       "holmes",
		Version:    version,
		Status:     "demo-analysis",
		Path:       clean,
		Bytes:      len(bytes),
		SHA256:     hex.EncodeToString(sum[:]),
		Lines:      countLines(text),
		Words:      len(strings.Fields(text)),
		Components: []string{"ingestion", "linguistic-primitives", "evidence"},
	}
	record.EvidenceRef = "evidence://holmes/" + stableID(record.SHA256)
	return record, nil
}

func countLines(text string) int {
	if text == "" {
		return 0
	}
	count := strings.Count(text, "\n")
	if !strings.HasSuffix(text, "\n") {
		count++
	}
	return count
}

func runEvidence(command, status string, details map[string]any) {
	printJSON(evidence{
		Tool:      "holmes",
		Version:   version,
		Commit:    commit,
		BuildDate: date,
		Repo:      "SocioProphet/holmes",
		Command:   command,
		Status:    status,
		Details:   details,
	})
}

func stableID(value string) string {
	sum := sha256.Sum256([]byte(value))
	return hex.EncodeToString(sum[:])[:16]
}

func printJSON(value any) {
	enc := json.NewEncoder(os.Stdout)
	enc.SetIndent("", "  ")
	if err := enc.Encode(value); err != nil {
		panic(errors.New("failed to encode JSON: " + err.Error()))
	}
}
