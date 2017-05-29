
import requests
import json
import textwrap

CATEGORIES = [
    # Categories
    # ----------
    # Uncomment the categories you are interested in

    # "ACA",    # Affordable Care Act
    "AG",     # Agriculture
    # "AR",     # Arts (see 'Cultural Affairs' in CFDA)
    # "BC",     # Business and Commerce
    "CD",     # Community Development
    # "CP",     # Consumer Protection
    "DPR",    # Disaster Prevention and Relief
    # "ED",     # Education
    "ELT",    # Employment, Labor and Training
    # "EN",     # Energy
    "ENV",    # Environment
    "FN",     # Food and Nutrition
    # "HL",     # Health
    # "HO",     # Housing
    # "HU",     # Humanities (see 'Cultural Affairs' in CFDA)
    # "ISS",    # Income Security and Social Services
    # "IS",     # Information and Statistics
    # "LJL",    # Law, Justice and Legal Services
    # "NR",     # Natural Resources
    # "O",      # Other (see text field entitled 'Explanation of Other Category of Funding Activity' for clarification)
    # "RA",     # Recovery Act
    "RD",     # Regional Development
    # "ST",     # Science and Technology and other Research and Development
    # "T",      # Transportation
]

def load_seen():
    try:
        with open('./seen.lst', 'r') as f:
            for line in f:
                yield line[:-1]
    except FileNotFoundError:
        return


def mark_seen(doc_id):
    with open('./seen.lst', 'a') as f:
        f.write("{}\n".format(doc_id))


def save(doc_id):
    with open('./saved.lst', 'a') as f:
        f.write("{}\n".format(grant_url(doc_id)))


def yes_or_no(prompt):
    ch = input(prompt)
    return ch not in ['n', 'N']


def load_details(opp_id):
    return requests.post("https://www.grants.gov/grantsws/rest/opportunity/details", data={'oppId': opp_id}).json()


def load_opportunity_page(start_at=0):
    "|".join(CATEGORIES)
    parameters = {
        "startRecordNum":start_at,
        "oppStatuses":"forecasted|posted",
        "sortBy":"oppNum|asc",
        "fundingCategories":"|".join(CATEGORIES),
        "eligibilities":"12|13|21|22|23|25|99"
    }
    response = requests.post("https://www.grants.gov/grantsws/rest/opportunities/search/", data=json.dumps(parameters))
    results = response.json()
    return results['oppHits']


def load_opportunities():
    start_at=0
    has_more = True
    while has_more:
        page = load_opportunity_page(start_at)
        has_more = len(page) == 25
        for hit in page:
            start_at += 1
            yield hit


def grant_url(grant_id):
    return "https://www.grants.gov/web/grants/view-opportunity.html?oppId={}".format(grant_id)


def main():
    seen = set(load_seen())
    for hit in load_opportunities():
        if hit['id'] in seen:
            continue

        print("==============================================")
        print("Title: {}".format(hit['title']))
        if yes_or_no("Explore (Yn)?") is False:
            mark_seen(hit['id'])
            continue

        details = load_details(hit['id'])

        synopsis = details['synopsis']
        print("URL:          {}".format(grant_url(hit['id'])))
        print("Max award:    {}".format(synopsis.get('awardCeiling', "N/A")))
        print("Agency:       {}".format(synopsis.get('agencyName', "N/A")))
        print("Cost Sharing: {}".format('yes' if synopsis['costSharing'] else 'no'))
        print()
        print("Applicant types:")
        print("\n".join(["    - " + d['description'] for d in synopsis['applicantTypes']]))
        print()
        print("Description:")
        print("    " + "\n    ".join(textwrap.wrap(synopsis['synopsisDesc'], 100)))
        print()

        if yes_or_no("Save (Yn)?") is False:
            mark_seen(hit['id'])
            continue

        save(hit['id'])
        mark_seen(hit['id'])

if __name__ == '__main__':
    main()
