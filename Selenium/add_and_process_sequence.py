from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

import random
import string
import time
import sys


# random strings

def random_chars(size = None, chars=string.ascii_lowercase):
    size = random.randint(3, 10) if size is None else size
    return ''.join(random.choice(chars) for _ in range(size))

def random_proper():
    return random_chars(size=1, chars=string.ascii_uppercase) + random_chars()

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

host_address = "http://localhost:5000/"

def init():
    global host_address
    # Create a new instance of the Firefox driver
    #driver.implicitly_wait(5)

    # go to the home page
    if len(sys.argv) > 1:
        host_address = sys.argv[1]

    driver.get(host_address)

    # make sure we are logged out
    try:
        if driver.find_element_by_partial_link_text("Logout"):
            driver.find_element_by_partial_link_text("Logout").click()
    except NoSuchElementException:
        pass


def main():
    init()


    driver.find_element_by_link_text("Login").click()
    driver.find_element_by_name("email").send_keys('fred@lees.org.uk')
    driver.find_element_by_name("password").send_keys('123456')
    driver.find_element_by_name("submit").click()

    driver.find_element_by_link_text("Sequences").click()
    sub_add_and_process()

def sub_add_and_process():
    # Create a new sequence
    driver.find_element_by_link_text("New Sequence").click()
    wait.until(EC.element_to_be_clickable((By.ID,'new_name')))
    name = random_proper()
    driver.find_element_by_id("new_name").send_keys(name)

    # Select an available inferred sequence from the submissions

    sel_sub = Select(driver.find_element_by_id('submission_id'))
    sub_opts = sel_sub.options

    for sub_opt in sub_opts[1:]:
        sub_opt.click()
        time.sleep(3)
        sel_seq = Select(driver.find_element_by_id('sequence_name'))
        seq_opts = sel_seq.options

        if len(seq_opts) > 0:
            seq_opts[0].click()
            break

    time.sleep(3)
    driver.find_element_by_id('create').click()

    # Edit the new sequence and add the IMGT alignment

    driver.find_element_by_link_text("Sequences").click()
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, name)))
    element = driver.find_element_by_link_text(name)
    element = element.find_element(By.XPATH, "//*[text()[.='%s']]/following-sibling::a" % name).click()

    wait.until(EC.element_to_be_clickable((By.ID, 'coding_seq_imgt')))
    driver.find_element_by_name("coding_seq_imgt").send_keys("""caggtgcagctggtgcagtctggggct...gaggtgaagaagcctggggcctcagtgaag
gtctcctgcaaggcttctggatacaccttc............accggctactatatgcac
tgggtgcgacaggcccctggacaagggcttgagtggatgggatggatcaaccctaac...
...agtggtggcacaaactatgcacagaagtttcag...ggcagggtcaccatgaccagg
gacacgtccatcagcacagcctacatggagctgagcaggctgagatctgacgacacggcc
gtgtattactgtgcgagaga""")

    # Add another inferred sequence from the edit screen

    driver.find_element_by_xpath('//*[@id="tab-inf"]').click()
    wait.until(EC.element_to_be_clickable((By.ID,'add_inference_btn')))
    driver.find_element_by_id('add_inference_btn').click()

    wait.until(EC.element_to_be_clickable((By.ID, 'submission_id')))
    time.sleep(3)
    sel_sub = Select(driver.find_element_by_id('submission_id'))
    sub_opts = sel_sub.options

    for sub_opt in sub_opts[1:]:
        sub_opt.click()
        time.sleep(3)
        sel_seq = Select(driver.find_element_by_id('sequence_name'))
        seq_opts = sel_seq.options

        if len(seq_opts) > 0:
            seq_opts[0].click()
            break

    time.sleep(3)
    driver.find_element_by_id('create').click()

    # Check the number of inferred sequences and delete one

    wait.until(EC.element_to_be_clickable((By.ID,'add_inference_btn')))
    x = driver.find_elements(By.XPATH, '//*[contains(@class, "delbutton")]')
    assert(len(x) == 2)
    x[random.randint(0, len(x)-1)].click()
    time.sleep(1)
    wait.until(EC.element_to_be_clickable((By.ID,'add_inference_btn')))

    # Add some acknowledgements

    driver.find_element_by_xpath('//*[@id="tab-ack"]').click()
    nitems = random.randint(3,5)
    names = [random_proper() + ' ' + random_proper() for i in range(nitems) ]
    insts = [random_proper() + ' ' + random_proper() for i in range(nitems) ]
    orcids = ['0000-0001-9834-6840' if i < (nitems/2) else '' for i in range(nitems)  ]
    for i in range(nitems):
        wait.until(EC.element_to_be_clickable((By.ID,'ack_name')))
        driver.find_element_by_id("ack_name").send_keys(names[i])
        driver.find_element_by_id("ack_institution_name").send_keys(insts[i])
        driver.find_element_by_id("ack_ORCID_id").send_keys(orcids[i])
        driver.find_element_by_id("add_ack").click()

    wait.until(EC.element_to_be_clickable((By.XPATH,'//*[contains(@id, "ack_del_")]')))
    x = driver.find_elements(By.XPATH, '//*[contains(@id, "ack_del_")]')
    assert(len(x) == nitems)
    i = random.randint(0, nitems-1)
    x[i].click()
    wait.until(EC.element_to_be_clickable((By.XPATH,'//*[contains(@id, "ack_del_")]')))
    x = driver.find_elements(By.XPATH, '//*[contains(@id, "ack_del_")]')
    assert(len(x) == nitems-1)

    # Add a note

    driver.find_element_by_xpath('//*[@id="tab-notes"]').click()

    wait.until(EC.element_to_be_clickable((By.ID,'notes')))
    driver.find_element_by_id('notes').send_keys(random_chars(size=random.randint(50,500), chars=string.ascii_lowercase + ' '))
    wait.until(EC.element_to_be_clickable((By.ID,'save_draft_btn')))
    driver.find_element_by_id('save_draft_btn').click()

    # View the draft, and pop up both sequence views

    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, name)))
    driver.find_element_by_link_text(name).click()

    wait.until(EC.element_to_be_clickable((By.ID, 'seq_view'))).click()
    time.sleep(3)

    wait.until(EC.element_to_be_clickable((By.CLASS_NAME,'btn-default'))).click()
    time.sleep(3)

    wait.until(EC.element_to_be_clickable((By.ID, 'seq_coding_view'))).click()
    time.sleep(3)

    wait.until(EC.element_to_be_clickable((By.CLASS_NAME,'btn-default'))).click()
    time.sleep(3)

    # Go back to Edit again, and publish

    driver.find_element_by_link_text("Sequences").click()
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, name)))
    element = driver.find_element_by_link_text(name)
    element = element.find_element(By.XPATH, "//*[text()[.='%s']]/following-sibling::a" % name).click()

    wait.until(EC.element_to_be_clickable((By.ID, 'publish_btn')))
    driver.find_element_by_id('publish_btn').click()
    wait.until(EC.element_to_be_clickable((By.ID,'body'))).send_keys('Completed')
    wait.until(EC.element_to_be_clickable((By.ID, 'history_btn'))).click()

    # New draft

    driver.find_element(By.XPATH, "//*[text()[.='%s']]/following-sibling::button" % name).click()
    time.sleep(3)
    el = driver.find_element_by_class_name('btn-warning')
    el.click()

    # Promote

    time.sleep(3)
    element = driver.find_element_by_link_text(name)
    element = element.find_element(By.XPATH, "//*[text()[.='%s']]/following-sibling::a" % name).click()
    wait.until(EC.element_to_be_clickable((By.ID, 'publish_btn')))
    driver.find_element_by_id('publish_btn').click()
    wait.until(EC.element_to_be_clickable((By.ID,'body'))).send_keys('Completed')
    wait.until(EC.element_to_be_clickable((By.ID, 'history_btn'))).click()

    # Withdraw

    driver.find_element(By.XPATH, "//*[text()[.='%s']]/following-sibling::button[2]" % name).click()
    time.sleep(3)
    el = driver.find_element_by_class_name('btn-danger')
    el.click()


def sub_del(sub_id):
    driver.find_element_by_id(sub_id).click()
    time.sleep(2)
    el = driver.find_element_by_class_name('btn-danger')
    time.sleep(2)
    el.click()


def sub_edit_ack():
    nitems = random.randint(3,10)
    names = [random_proper() + ' ' + random_proper() for i in range(nitems) ]
    insts = [random_proper() + ' ' + random_proper() for i in range(nitems) ]
    orcids = ['0000-0001-9834-6840' if i < (nitems/2) else '' for i in range(nitems)  ]

    driver.find_element_by_xpath('//*[@id="tab-ack"]').click()

    pmids = ['23454', '12345', '75435', '87654']
    n_pmids = random.randint(2, len(pmids)-1)

    for i in range(n_pmids):
        wait.until(EC.element_to_be_clickable((By.ID,'pubmed_id')))
        driver.find_element_by_id("pubmed_id").send_keys(pmids[i])
        driver.find_element_by_id("add_pubmed").click()

    wait.until(EC.element_to_be_clickable((By.XPATH,'//*[contains(@id, "pubmed_del_")]')))
    x = driver.find_elements(By.XPATH, '//*[contains(@id, "pubmed_del_")]')
    assert(len(x) == n_pmids)
    i = random.randint(0, n_pmids-1)
    x[i].click()
    wait.until(EC.element_to_be_clickable((By.XPATH,'//*[contains(@id, "pubmed_del_")]')))
    x = driver.find_elements(By.XPATH, '//*[contains(@id, "pubmed_del_")]')
    assert(len(x) == n_pmids-1)

    for i in range(nitems):
        wait.until(EC.element_to_be_clickable((By.ID,'ack_name')))
        driver.find_element_by_id("ack_name").send_keys(names[i])
        driver.find_element_by_id("ack_institution_name").send_keys(insts[i])
        driver.find_element_by_id("ack_ORCID_id").send_keys(orcids[i])
        driver.find_element_by_id("add_ack").click()

    wait.until(EC.element_to_be_clickable((By.XPATH,'//*[contains(@id, "ack_del_")]')))
    x = driver.find_elements(By.XPATH, '//*[contains(@id, "ack_del_")]')
    assert(len(x) == nitems)
    i = random.randint(0, nitems-1)
    x[i].click()
    wait.until(EC.element_to_be_clickable((By.XPATH,'//*[contains(@id, "ack_del_")]')))
    x = driver.find_elements(By.XPATH, '//*[contains(@id, "ack_del_")]')
    assert(len(x) == nitems-1)

    return nitems-1


def sub_edit_rep(sub_id):
    driver.find_element_by_xpath('//*[@id="tab-rep"]').click()

    wait.until(EC.element_to_be_clickable((By.ID,"repository_name")))
    driver.find_element_by_id("repository_name").send_keys('NIH')
    driver.find_element_by_id("rep_accession_no").send_keys('SRA'+ random_chars(size = 5, chars=string.digits))
    driver.find_element_by_id("dataset_url").send_keys('https://trace.ncbi.nlm.nih.gov/Traces/sra/?study=ERP108969')
    driver.find_element_by_id("sequencing_platform").send_keys('Illumina MiSeq')
    driver.find_element_by_id("read_length").send_keys('250x250bp')

    driver.find_element_by_name("save_btn").click()
    driver.get(host_address + "edit_submission/" + sub_id)
    wait.until(EC.element_to_be_clickable((By.NAME,'save_btn')))


def sub_edit_pri():
    driver.find_element_by_xpath('//*[@id="tab-pri"]').click()

    wait.until(EC.element_to_be_clickable((By.ID,'upload_fw')))
    driver.find_element_by_id("upload_fw").click()
    wait.until(EC.element_to_be_clickable((By.ID,'btn-upload')))
    driver.find_element_by_id("sel-file").send_keys("D:\\Research\\ogre\\testfiles\\R1_lim_primers.fasta")
    driver.find_element_by_id("btn-upload").click()
    time.sleep(2)
    wait.until(EC.element_to_be_clickable((By.ID,'upload_rv')))
    time.sleep(2)
    x = driver.find_elements(By.XPATH, '//*[contains(@id, "fw_primer_del_")]')
    assert(len(x) == 20)
    x[random.randint(0, 19)].click()
    x = driver.find_elements(By.XPATH, '//*[contains(@id, "fw_primer_del_")]')
    assert(len(x) == 19)
    driver.find_element_by_id("fw_primer_name").send_keys(random_proper())
    driver.find_element_by_id("fw_primer_seq").send_keys(random_chars(random.randint(10,30), chars='AGCTRYSWKMBDHVN'))
    driver.find_element_by_id('add_fw_primer').click()
    wait.until(EC.element_to_be_clickable((By.ID,'add_fw_primer')))
    x = driver.find_elements(By.XPATH, '//*[contains(@id, "fw_primer_del_")]')
    assert(len(x) == 20)

    driver.find_element_by_id("upload_rv").click()
    time.sleep(2)
    wait.until(EC.element_to_be_clickable((By.ID,'btn-upload')))
    driver.find_element_by_id("sel-file").send_keys("D:\\Research\\ogre\\testfiles\\R2_300_primers_inc_light.fasta")
    driver.find_element_by_id("btn-upload").click()
    time.sleep(2)
    wait.until(EC.element_to_be_clickable((By.ID,'upload_rv')))
    time.sleep(2)
    x = driver.find_elements(By.XPATH, '//*[contains(@id, "rv_primer_del_")]')
    assert(len(x) == 4)
    x[random.randint(0, 3)].click()
    x = driver.find_elements(By.XPATH, '//*[contains(@id, "rv_primer_del_")]')
    assert(len(x) == 3)
    driver.find_element_by_id("rv_primer_name").send_keys(random_proper())
    driver.find_element_by_id("rv_primer_seq").send_keys(random_chars(random.randint(10,30), chars='AGCTRYSWKMBDHVN'))
    driver.find_element_by_id('add_rv_primer').click()
    wait.until(EC.element_to_be_clickable((By.ID,'add_rv_primer')))
    x = driver.find_elements(By.XPATH, '//*[contains(@id, "rv_primer_del_")]')
    assert(len(x) == 4)

def sub_edit_notes(sub_id):
    driver.find_element_by_xpath('//*[@id="tab-notes"]').click()

    wait.until(EC.element_to_be_clickable((By.ID,'notes_text')))
    driver.find_element_by_id('notes_text').send_keys(random_chars(size=random.randint(50,500), chars=string.ascii_lowercase + ' '))

    driver.find_element_by_id('notes_attachment').send_keys("D:\\Research\\ogre\\testfiles\\genotype_1.csv")

    driver.find_element_by_name("save_btn").click()
    driver.get(host_address + "edit_submission/" + sub_id)
    wait.until(EC.element_to_be_clickable((By.NAME,'save_btn')))


def sub_edit_inf():
    driver.find_element_by_xpath('//*[@id="tab-inf"]').click()

    wait.until(EC.element_to_be_clickable((By.ID,'add_tools')))

    nitems = random.randint(2,4)

    for _ in range(nitems):
        driver.find_element_by_id('add_tools').click()
        wait.until(EC.element_to_be_clickable((By.ID,'tool_settings_name')))
        driver.find_element_by_id('tool_settings_name').send_keys(random_proper())
        driver.find_element_by_id('tool_name').send_keys(random_proper())
        driver.find_element_by_id('tool_version').send_keys(random_chars(size=random.randint(1,4), chars=string.digits))
        driver.find_element_by_id('tool_starting_database').send_keys(random_chars(size=random.randint(50,200), chars=string.ascii_lowercase + ' '))
        driver.find_element_by_id('tool_settings').send_keys(random_chars(size=random.randint(50,500), chars=string.ascii_lowercase + ' '))
        driver.find_element_by_id('save-btn').click()
        wait.until(EC.element_to_be_clickable((By.ID,'add_tools')))

    x = driver.find_elements(By.XPATH, '//*[contains(@id, "delete_tool")]')
    assert(len(x) == nitems)
    x[random.randint(0,nitems-1)].click()
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME,'btn-danger'))).click()
    time.sleep(2)
    wait.until(EC.element_to_be_clickable((By.ID,'add_tools')))
    x = driver.find_elements(By.XPATH, '//*[contains(@id, "delete_tool")]')
    assert(len(x) == nitems-1)

    wait.until(EC.element_to_be_clickable((By.ID,'add_tools')))
    x = driver.find_elements(By.CLASS_NAME, 'text-warning')
    x[random.randint(0,nitems-2)].click()
    wait.until(EC.element_to_be_clickable((By.ID,'tool_settings_name')))
    driver.find_element_by_id('tool_settings_name').send_keys(random_proper())
    driver.find_element_by_id('save-btn').click()
    wait.until(EC.element_to_be_clickable((By.ID,'add_tools')))


def sub_edit_gen():
    driver.find_element_by_xpath('//*[@id="tab-gen"]').click()
    wait.until(EC.element_to_be_clickable((By.ID,'add_genotype_description')))

    nitems = random.randint(2,4)
    for _ in range(nitems):
        driver.find_element_by_id('add_genotype_description').click()
        wait.until(EC.element_to_be_clickable((By.ID,'genotype_name')))
        driver.find_element_by_id('genotype_name').send_keys(random_proper())
        driver.find_element_by_id('genotype_subject_id').send_keys(random_chars(size=random.randint(1,4), chars=string.digits))
        ids = ','.join(['SAMN' + random_chars(size=8, chars=string.digits) for _ in range(random.randint(1,10))])
        driver.find_element_by_id('genotype_biosample_ids').send_keys(ids)
        sel = Select(driver.find_element_by_id('inference_tool_id'))
        opts = sel.options
        opts[random.randint(0,len(opts)-1)].click()
        driver.find_element_by_id('genotype_file').send_keys("D:\\Research\\ogre\\testfiles\\genotype_1.csv")
        driver.find_element_by_id('save_genotype').click()
        wait.until(EC.element_to_be_clickable((By.ID,'add_genotype_description')))

    x = driver.find_elements(By.XPATH, '//*[contains(@href, "edit_genotype")]')
    assert(len(x) == nitems)
    x[random.randint(0,nitems-1)].click()
    wait.until(EC.element_to_be_clickable((By.ID,'genotype_name')))
    driver.find_element_by_id('genotype_name').send_keys(random_proper())
    driver.find_element_by_id('save_genotype').click()
    wait.until(EC.element_to_be_clickable((By.ID,'add_genotype_description')))

    x = driver.find_elements(By.XPATH, '//*[contains(@href, "genotype/")]')
    assert(len(x) == nitems)
    x[random.randint(0,nitems-1)].click()
    wait.until(EC.element_to_be_clickable((By.ID,'download_genotype')))
    driver.execute_script("window.history.go(-1)")
    wait.until(EC.element_to_be_clickable((By.ID,'add_genotype_description')))

    x = driver.find_elements(By.XPATH, '//*[contains(@id, "delete_gen")]')
    assert(len(x) == nitems)
    x[random.randint(0,nitems-1)].click()
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME,'btn-danger'))).click()
    time.sleep(2)
    wait.until(EC.element_to_be_clickable((By.ID,'add_genotype_description')))
    x = driver.find_elements(By.XPATH, '//*[contains(@id, "delete_gen")]')
    assert(len(x) == nitems-1)


def sub_edit_seq():
    driver.find_element_by_xpath('//*[@id="tab-seq"]').click()
    wait.until(EC.element_to_be_clickable((By.ID,'add_inferred_sequence')))

    nitems = random.randint(2,4)

    selected_seqs = []

    for _ in range(nitems):
        driver.find_element_by_id('add_inferred_sequence').click()
        wait.until(EC.element_to_be_clickable((By.ID,'seq_accession_no')))
        sel = Select(driver.find_element_by_id('genotype_id'))
        opts = sel.options
        opts[random.randint(0,len(opts)-1)].click()
        time.sleep(4)

        driver.find_element_by_id('seq_accession_no').send_keys('SRX' + random_chars(size=8, chars=string.digits))
        driver.find_element_by_id('deposited_version').send_keys(random_chars(size=2, chars=string.digits))
        ids = ','.join(['SRR' + random_chars(size=8, chars=string.digits) for _ in range(random.randint(1,10))])
        driver.find_element_by_id('run_ids').send_keys(ids)

        wait.until(EC.element_to_be_clickable((By.ID,'sequence_id')))
        sel = Select(driver.find_element_by_id('sequence_id'))
        opts = sel.options

        while True:
            selected_seq = random.randint(0,len(opts)-1)
            if selected_seq not in selected_seqs:
                selected_seqs.append(selected_seq)
                opt = opts[selected_seq]
                break

        opt.click()
        time.sleep(2)

        if random.randint(0,2) > 0:
            driver.find_element_by_id('inferred_extension').click()
            wait.until(EC.element_to_be_clickable((By.ID,'ext_3prime')))
            driver.find_element_by_id('ext_3prime').send_keys('acgt')
            driver.find_element_by_id('start_3prime_ext').send_keys('20')
            driver.find_element_by_id('end_3prime_ext').send_keys('23')

        wait.until(EC.element_to_be_clickable((By.ID,'sequence_id')))
        time.sleep(2)
        driver.find_element_by_id('save_sequence').click()
        wait.until(EC.element_to_be_clickable((By.ID,'add_inferred_sequence')))

    x = driver.find_elements(By.XPATH, '//*[contains(@href, "edit_inferred")]')
    assert(len(x) == nitems)
    x[random.randint(0,nitems-1)].click()
    wait.until(EC.element_to_be_clickable((By.ID,'seq_accession_no')))
    driver.find_element_by_id('seq_accession_no').send_keys('SRX' + random_chars(size=8, chars=string.digits))
    driver.find_element_by_id('save_sequence').click()
    wait.until(EC.element_to_be_clickable((By.ID,'add_inferred_sequence')))

    x = driver.find_elements(By.XPATH, '//*[contains(@id, "inferred_sequence_del")]')
    assert(len(x) == nitems)
    x[random.randint(0,nitems-1)].click()
    time.sleep(1)
    wait.until(EC.element_to_be_clickable((By.ID,'add_inferred_sequence')))
    x = driver.find_elements(By.XPATH, '//*[contains(@id, "inferred_sequence_del")]')
    assert(len(x) == nitems-1)


def sub_submit():
    time.sleep(3)
    current_handles = driver.window_handles
    driver.find_element_by_name('submit_btn').click()
    time.sleep(3)
    els = driver.find_elements_by_class_name('btn-warning')
    els[2].click()


def sub_review_actions(sub_id):
    wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, sub_id))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="tab-rev"]'))).click()
    wait.until(EC.element_to_be_clickable((By.ID, 'complete'))).click()

    wait.until(EC.element_to_be_clickable((By.ID,'body'))).send_keys('Completed')
    wait.until(EC.element_to_be_clickable((By.ID, 'save_btn'))).click()

    wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, sub_id))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="tab-rev"]'))).click()
    wait.until(EC.element_to_be_clickable((By.ID, 'ret_review'))).click()

    wait.until(EC.element_to_be_clickable((By.ID,'body'))).send_keys('Un-Completed')
    wait.until(EC.element_to_be_clickable((By.ID, 'save_btn'))).click()

    wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, sub_id))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="tab-rev"]'))).click()
    wait.until(EC.element_to_be_clickable((By.ID, 'draft'))).click()

    wait.until(EC.element_to_be_clickable((By.ID,'body'))).send_keys('Returned')
    wait.until(EC.element_to_be_clickable((By.ID, 'save_btn'))).click()


if __name__=="__main__":
    main()
    pass



