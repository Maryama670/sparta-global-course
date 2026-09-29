"""The document corpus. SYNTHETIC PLACEHOLDER CONTENT ONLY.

Unlike data.py, which holds structured records, this holds prose - the kind of
unstructured text a client would actually have sitting in SharePoint.
"""

from typing import Any  # Import Any to allow document dictionary values to have different types.

DOCUMENTS: list[dict[str, Any]] = [  # Define the sample document corpus and its metadata.
    {  # Start a nested record.
        "id": "doc-001",  # Include the record identifier in this record.
        "title": "Harding & Voss — Market Position Note",  # Include the document title in this record.
        "firm_id": 1,  # Include the related firm identifier in this record.
        "type": "market-note",  # Include the document category in this record.
        "body": (  # Include the document text in this record.
            "Harding & Voss remains one of the stronger mid-tier performers in the UK "  # Continue the document body; adjacent strings are joined into one value.
            "market. Revenue growth has been steady rather than spectacular, and the "  # Continue the document body; adjacent strings are joined into one value.
            "firm has resisted the temptation to chase headline lateral hires. Its "  # Continue the document body; adjacent strings are joined into one value.
            "disputes practice is widely regarded as the strongest part of the "  # Continue the document body; adjacent strings are joined into one value.
            "business, particularly in commercial litigation and international "  # Continue the document body; adjacent strings are joined into one value.
            "arbitration. The corporate team is competent but has not won a "  # Continue the document body; adjacent strings are joined into one value.
            "significant mandate outside the UK in the last eighteen months. "  # Continue the document body; adjacent strings are joined into one value.
            "Partner retention is good. The firm does not operate in the United States "  # Continue the document body; adjacent strings are joined into one value.
            "and has no plans to open there."  # Continue the document body; adjacent strings are joined into one value.
        ),  # Close the preceding expression or collection.
    },  # Close the preceding expression or collection.
    {  # Start a nested record.
        "id": "doc-002",  # Include the record identifier in this record.
        "title": "Marchetti Ruiz — Compensation Review",  # Include the document title in this record.
        "firm_id": 2,  # Include the related firm identifier in this record.
        "type": "compensation",  # Include the document category in this record.
        "body": (  # Include the document text in this record.
            "Marchetti Ruiz operates a modified lockstep model with a significant "  # Continue the document body; adjacent strings are joined into one value.
            "discretionary element at the top of the equity. This has allowed the firm "  # Continue the document body; adjacent strings are joined into one value.
            "to compete for high performers without abandoning its collegiate culture "  # Continue the document body; adjacent strings are joined into one value.
            "entirely. Profit per equity partner has grown consistently, though the "  # Continue the document body; adjacent strings are joined into one value.
            "gap between the top and bottom of equity has widened to a ratio that some "  # Continue the document body; adjacent strings are joined into one value.
            "partners consider unsustainable. The firm's US practice drives the "  # Continue the document body; adjacent strings are joined into one value.
            "majority of profitability. Associate compensation was reviewed in the "  # Continue the document body; adjacent strings are joined into one value.
            "last cycle and brought broadly in line with the market."  # Continue the document body; adjacent strings are joined into one value.
        ),  # Close the preceding expression or collection.
    },  # Close the preceding expression or collection.
    {  # Start a nested record.
        "id": "doc-003",  # Include the record identifier in this record.
        "title": "Okonkwo Bell — Strategy Briefing",  # Include the document title in this record.
        "firm_id": 3,  # Include the related firm identifier in this record.
        "type": "strategy",  # Include the document category in this record.
        "body": (  # Include the document text in this record.
            "Okonkwo Bell is a boutique with a deliberately narrow focus. The firm has "  # Continue the document body; adjacent strings are joined into one value.
            "built a reputation in energy and infrastructure work, particularly "  # Continue the document body; adjacent strings are joined into one value.
            "projects with a development finance element. It is not trying to be a "  # Continue the document body; adjacent strings are joined into one value.
            "full-service firm and has turned away work outside its core areas. "  # Continue the document body; adjacent strings are joined into one value.
            "Headcount has grown slowly and deliberately. The firm's leadership has "  # Continue the document body; adjacent strings are joined into one value.
            "been explicit that it does not intend to merge, and has declined at least "  # Continue the document body; adjacent strings are joined into one value.
            "two approaches in the past three years."  # Continue the document body; adjacent strings are joined into one value.
        ),  # Close the preceding expression or collection.
    },  # Close the preceding expression or collection.
    {  # Start a nested record.
        "id": "doc-004",  # Include the record identifier in this record.
        "title": "Sandoval Kerr — Risk and Compliance Summary",  # Include the document title in this record.
        "firm_id": 4,  # Include the related firm identifier in this record.
        "type": "compliance",  # Include the document category in this record.
        "body": (  # Include the document text in this record.
            "Sandoval Kerr has invested heavily in its conflicts and compliance "  # Continue the document body; adjacent strings are joined into one value.
            "function following a difficult period two years ago. The firm's matter "  # Continue the document body; adjacent strings are joined into one value.
            "intake process now requires sign-off from a dedicated risk partner for "  # Continue the document body; adjacent strings are joined into one value.
            "any engagement above a defined threshold. Professional indemnity "  # Continue the document body; adjacent strings are joined into one value.
            "arrangements were renegotiated at the last renewal. There are no "  # Continue the document body; adjacent strings are joined into one value.
            "outstanding regulatory matters. The firm reports no material claims "  # Continue the document body; adjacent strings are joined into one value.
            "in the current period."  # Continue the document body; adjacent strings are joined into one value.
        ),  # Close the preceding expression or collection.
    },  # Close the preceding expression or collection.
    {  # Start a nested record.
        "id": "doc-005",  # Include the record identifier in this record.
        "title": "Lindqvist Partners — APAC Expansion Review",  # Include the document title in this record.
        "firm_id": 5,  # Include the related firm identifier in this record.
        "type": "strategy",  # Include the document category in this record.
        "body": (  # Include the document text in this record.
            "Lindqvist Partners has grown its Singapore office faster than any other "  # Continue the document body; adjacent strings are joined into one value.
            "part of the business. The firm's APAC strategy leans on relationships "  # Continue the document body; adjacent strings are joined into one value.
            "with Nordic corporates operating in the region rather than on local "  # Continue the document body; adjacent strings are joined into one value.
            "market share. This has produced a profitable but narrow practice. The "  # Continue the document body; adjacent strings are joined into one value.
            "Tokyo office has underperformed against its original business case and "  # Continue the document body; adjacent strings are joined into one value.
            "is under review. Matter reference LP-2291 covers the internal assessment "  # Continue the document body; adjacent strings are joined into one value.
            "of that review and is not for external circulation."  # Continue the document body; adjacent strings are joined into one value.
        ),  # Close the preceding expression or collection.
    },  # Close the preceding expression or collection.
    {  # Start a nested record.
        "id": "doc-006",  # Include the record identifier in this record.
        "title": "UK Market Commentary — Lateral Hiring",  # Include the document title in this record.
        "firm_id": None,  # Include the related firm identifier in this record.
        "type": "market-note",  # Include the document category in this record.
        "body": (  # Include the document text in this record.
            "Lateral partner hiring across the UK market slowed in the most recent "  # Continue the document body; adjacent strings are joined into one value.
            "period, reversing three years of aggressive recruitment. Firms that "  # Continue the document body; adjacent strings are joined into one value.
            "over-extended on guaranteed packages are now carrying underperforming "  # Continue the document body; adjacent strings are joined into one value.
            "partners they cannot easily exit. The firms that held their discipline "  # Continue the document body; adjacent strings are joined into one value.
            "are in a materially better position. Disputes practices continue to "  # Continue the document body; adjacent strings are joined into one value.
            "attract the most competitive offers, while transactional teams have seen "  # Continue the document body; adjacent strings are joined into one value.
            "offers flatten."  # Continue the document body; adjacent strings are joined into one value.
        ),  # Close the preceding expression or collection.
    },  # Close the preceding expression or collection.
    {  # Start a nested record.
        "id": "doc-007",  # Include the record identifier in this record.
        "title": "Jurisdiction Note — EU Practice Rights",  # Include the document title in this record.
        "firm_id": None,  # Include the related firm identifier in this record.
        "type": "regulatory",  # Include the document category in this record.
        "body": (  # Include the document text in this record.
            "Firms operating across EU member states continue to navigate divergent "  # Continue the document body; adjacent strings are joined into one value.
            "requirements on practice rights and establishment. The position for "  # Continue the document body; adjacent strings are joined into one value.
            "UK-qualified lawyers has not returned to the pre-2021 arrangement. Firms "  # Continue the document body; adjacent strings are joined into one value.
            "with a registered EU presence are largely unaffected. Those servicing EU "  # Continue the document body; adjacent strings are joined into one value.
            "clients from London face more friction, particularly in regulated "  # Continue the document body; adjacent strings are joined into one value.
            "advisory work. Reference EUPR-14 sets out the current position per "  # Continue the document body; adjacent strings are joined into one value.
            "jurisdiction."  # Continue the document body; adjacent strings are joined into one value.
        ),  # Close the preceding expression or collection.
    },  # Close the preceding expression or collection.
    {  # Start a nested record.
        "id": "doc-008",  # Include the record identifier in this record.
        "title": "Benchmarking Methodology",  # Include the document title in this record.
        "firm_id": None,  # Include the related firm identifier in this record.
        "type": "methodology",  # Include the document category in this record.
        "body": (  # Include the document text in this record.
            "Revenue per lawyer is calculated as total revenue divided by total "  # Continue the document body; adjacent strings are joined into one value.
            "fee-earner headcount, excluding business services staff. Profit per "  # Continue the document body; adjacent strings are joined into one value.
            "equity partner assumes a thirty-five per cent margin applied to revenue, "  # Continue the document body; adjacent strings are joined into one value.
            "then divided by the number of full equity partners. Fixed-share partners "  # Continue the document body; adjacent strings are joined into one value.
            "are excluded from that denominator. These figures are indicative and "  # Continue the document body; adjacent strings are joined into one value.
            "should not be compared across jurisdictions without adjustment for "  # Continue the document body; adjacent strings are joined into one value.
            "local cost bases."  # Continue the document body; adjacent strings are joined into one value.
        ),  # Close the preceding expression or collection.
    },  # Close the preceding expression or collection.
]  # Close the preceding expression or collection.