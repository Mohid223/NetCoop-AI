
import React, { useState } from "react";
import {
  Copy,
  Check,
  Braces,
  FileJson,
  Download,
  ChevronDown,
  ChevronRight,
} from "lucide-react";

export default function JsonTab({
  report = {},
  investigation = {},
  result = {},
}) {
  const [copied, setCopied] = useState(false);
  const [expanded, setExpanded] = useState(true);

  // Prefer the complete backend response.
  const jsonData =
    Object.keys(result).length > 0
      ? result
      : {
          report,
          autonomous_investigation: investigation,
        };

  const formattedJson = JSON.stringify(jsonData, null, 2);

  const copyJson = async () => {
    try {
      await navigator.clipboard.writeText(formattedJson);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (error) {
      console.error("Unable to copy JSON:", error);
    }
  };

  const downloadJson = () => {
    const blob = new Blob([formattedJson], {
      type: "application/json",
    });

    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");

    link.href = url;
    link.download = `netcoop-investigation-${Date.now()}.json`;

    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    URL.revokeObjectURL(url);
  };

  const sections = [
    {
      name: "Incident Report",
      value: jsonData.report,
    },
    {
      name: "Autonomous Investigation",
      value: jsonData.autonomous_investigation,
    },
    {
      name: "Agent Message Log",
      value: jsonData.message_log,
    },
  ];

  return (
    <div className="json-tab">
      <div className="json-page-header">
        <div>
          <span className="json-eyebrow">
            <Braces size={15} />
            RAW RESPONSE
          </span>

          <h2>JSON Output</h2>

          <p>
            Inspect the complete response received from the backend API.
          </p>
        </div>

        <div className="json-actions">
          <button onClick={copyJson} className="json-action-button">
            {copied ? <Check size={16} /> : <Copy size={16} />}
            {copied ? "Copied" : "Copy JSON"}
          </button>

          <button onClick={downloadJson} className="json-action-button">
            <Download size={16} />
            Download
          </button>
        </div>
      </div>

      <div className="json-summary">
        <div>
          <FileJson size={19} />
          <span>JSON Document</span>
        </div>

        <span>{formattedJson.length.toLocaleString()} characters</span>
      </div>

      <div className="json-section-list">
        {sections.map((section) => (
          <div className="json-section-item" key={section.name}>
            <div className="json-section-title">
              <span>{section.name}</span>

              <span>
                {section.value === undefined
                  ? "Not available"
                  : "Included"}
              </span>
            </div>
          </div>
        ))}
      </div>

      <div className="json-viewer">
        <div className="json-viewer-header">
          <div>
            <button
              className="json-expand-button"
              onClick={() => setExpanded(!expanded)}
              aria-label="Toggle JSON"
            >
              {expanded ? (
                <ChevronDown size={17} />
              ) : (
                <ChevronRight size={17} />
              )}
            </button>

            <FileJson size={17} />
            <strong>response.json</strong>
          </div>

          <span>Read only</span>
        </div>

        {expanded ? (
          <pre className="json-code">
            <code>{formattedJson}</code>
          </pre>
        ) : (
          <div className="json-collapsed">
            JSON response is collapsed.
          </div>
        )}
      </div>

      <div className="json-footer">
        <span>NetCoop AI API Response</span>
        <span>{Object.keys(jsonData).length} top-level fields</span>
      </div>
    </div>
  );
}
