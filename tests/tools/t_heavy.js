// The one list of heavy words (page and helper carry the same line). Test-only.
const HEAVY=/\b(?:kill(?:ing)? my ?self|kms|unalive\w*|suicid\w*|end(?:ing)? (?:my (?:own )?life|it all)|take my (?:own )?life|(?:want(?:ing)?|wanna) (?:to )?die|(?:don'?t|do not|dont) want to (?:live|be here|be alive|exist)|hurt(?:ing)? my ?self|harm(?:ing)? my ?self|self[- ]?harm\w*|no reason to live|better off dead)\b/i;
const norm=t=>String(t).replace(/[‘’ʼ]/g,"'");
const yes=['I have been feeling suicidal lately','suicide has crossed my mind','I keep self-harming','I am hurting myself again','I want to kill my self','I wanna die','I do not want to live anymore','I want to take my own life','I just want to end it all','I want to end my life','some days I don’t want to be here','I dont want to exist','kms','thinking about how to unalive myself','everyone would be better off dead without me','I could hurt myself','I keep thinking about self harm','I want to die','no reason to live'];
const no=['I am dying to see my sister again','the light is dying in the evenings','I want to live by the sea','I want to be here more often','I am so tired of my job','I hurt my knee','I could end the call','I want to end the job','the end of my life story chapter','self-care matters to me','I died laughing','I feel lost'];
let f=0;
yes.forEach(t=>{if(!HEAVY.test(norm(t))){f++;console.log('MISSED  ',t);}});
no.forEach(t=>{if(HEAVY.test(norm(t))){f++;console.log('WRONGLY ',t);}});
const OLD=/\b(kill myself|end my life|suicid|want to die|don'?t want to (live|be here)|hurt myself|self[- ]?harm|no reason to live)\b/i;
console.log('old list missed', yes.filter(t=>!OLD.test(norm(t))).length, 'of', yes.length, '| new list:', f, 'faults');
process.exit(f?1:0);
