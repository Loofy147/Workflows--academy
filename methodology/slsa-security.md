# Software Supply Chain Security with SLSA

This document outlines the methodology for securing the software supply chain using the SLSA (Supply-chain Levels for Software Artifacts) framework. It covers the core concepts of software supply chain security, the SLSA framework, and the tools we will use to achieve compliance.

## Core Concepts

Software supply chain security is the process of securing the software development lifecycle, from the source code to the final build artifact. It involves protecting against a variety of attacks, such as:

-   **Source code tampering:** Malicious code is injected into the source code.
-   **Build process tampering:** The build process is compromised to produce a malicious artifact.
-   **Dependency confusion:** A malicious package is downloaded from a public repository instead of the intended private package.

The SLSA framework is a set of standards and controls to prevent tampering, improve integrity, and secure packages and infrastructure in your projects, businesses, or enterprises. SLSA defines an incrementally adoptable set of levels which are defined in terms of increasing compliance and assurance.

## Tools

We have selected the following open-source tool for our SLSA-compliant build workflow:

-   **`slsa-framework/slsa-github-generator`:** This is the official, language-agnostic tool from the SLSA Framework project for generating SLSA Level 3 provenance in GitHub Actions.

## Workflow Structure

Our SLSA-compliant build workflow is structured as a GitHub Actions workflow. The workflow is triggered on the `release` event, specifically when a new release is `created`. It performs the following steps:

1.  **Build Application:** Builds the application binary.
2.  **Generate Provenance:** Uses the `slsa-framework/slsa-github-generator` action to generate a cryptographically signed SLSA provenance attestation for the binary.
3.  **Upload Artifacts:** Uploads both the application binary and its provenance file as assets to the GitHub release.
