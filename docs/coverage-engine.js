/**
 * SpectraSec Security Control Mapper — client-side coverage engine.
 * Mirrors src/control_mapper/coverage.py. CI parity fixtures should keep both engines aligned.
 */
const CONFIDENCE_RANK = { CONTEXTUAL: 1, SUPPORTING: 2, DIRECT: 3 };

function effectiveConfidence(framework, configured) {
  if (configured !== 'CONTEXTUAL') return configured;
  if (framework === 'ISO/IEC 27001:2022' || framework === 'SOC 2') return 'SUPPORTING';
  return 'CONTEXTUAL';
}

function calculateCoverage(records, observations) {
  const observed = new Map(
    observations
      .filter((o) => o.status !== 'NOT_APPLICABLE')
      .map((o) => [o.check_id, o]),
  );
  const buckets = new Map();

  for (const record of records) {
    const matched = (record.source_check_ids || [])
      .map((cid) => observed.get(cid))
      .filter(Boolean);
    if (!matched.length) continue;

    for (const ref of record.references) {
      const key = `${ref.framework}|||${ref.reference}`;
      if (!buckets.has(key)) {
        buckets.set(key, {
          framework: ref.framework,
          reference: ref.reference,
          title: ref.title,
          passes: new Set(),
          fails: new Set(),
          unknowns: new Set(),
          evidence: new Set(),
          confidences: [],
        });
      }
      const bucket = buckets.get(key);
      bucket.title = ref.title;
      bucket.confidences.push(effectiveConfidence(ref.framework, ref.confidence));

      for (const obs of matched) {
        if (obs.status === 'PASS') {
          bucket.passes.add(obs.check_id);
        } else if (obs.status === 'FAIL') {
          bucket.fails.add(obs.check_id);
          (record.evidence_needed || []).forEach((e) => bucket.evidence.add(e));
        } else if (obs.status === 'UNKNOWN' || obs.status === 'ERROR') {
          bucket.unknowns.add(obs.check_id);
          (record.evidence_needed || []).forEach((e) => bucket.evidence.add(e));
        }
      }
    }
  }

  const results = [];
  for (const bucket of buckets.values()) {
    const passes = [...bucket.passes].sort();
    const fails = [...bucket.fails].sort();
    const unknowns = [...bucket.unknowns].sort();
    let status;
    if (fails.length && passes.length) status = 'PARTIAL';
    else if (fails.length) status = 'GAP';
    else if (unknowns.length && passes.length) status = 'PARTIAL';
    else if (unknowns.length) status = 'UNKNOWN';
    else status = 'SUPPORTED';

    const confidence = bucket.confidences.reduce(
      (best, current) => (
        CONFIDENCE_RANK[current] > CONFIDENCE_RANK[best] ? current : best
      ),
      bucket.confidences[0],
    );

    results.push({
      framework: bucket.framework,
      reference: bucket.reference,
      title: bucket.title,
      status,
      confidence,
      supporting_checks: passes,
      failing_checks: fails,
      unknown_checks: unknowns,
      evidence_needed: [...bucket.evidence].sort(),
    });
  }

  return results.sort((a, b) => (
    a.framework === b.framework
      ? a.reference.localeCompare(b.reference)
      : a.framework.localeCompare(b.framework)
  ));
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = { calculateCoverage, effectiveConfidence };
}
