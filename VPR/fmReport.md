## Records seen (by type)

1. ADVERSE REACTION ASSESSMENT-120_86: 20
2. ADVERSE REACTION REPORTING-120_85: 9
3. GMRV VITAL MEASUREMENT-120_5: 132259
4. PATIENT ALLERGIES-120_8: 86
5. PATIENT-2: 20
6. PROBLEM-9000011: 871

## Model

1. ADVERSE REACTION ASSESSMENT-120_86 (20) - 140 assertions

... mandatory properties: 7/7 - _id, assessing_user, assessment_date_time, label, name, reaction_assessment, type

	1. _id: 20
	2. type: 20
	3. label: 20
	4. name: 20
	5. assessing_user: 20 (POINTER) **M**
	6. assessment_date_time: 20 (DATE) **M**
	7. label: 20 **M**
	8. reaction_assessment: 20 **M**

2. ADVERSE REACTION REPORTING-120_85 (9) - 404 assertions

... mandatory properties: 10/39 - _id, date_time_of_event, label, observer, patient, reactions, related_reaction, severity, suspected_agent, type

	1. _id: 9
	2. type: 9
	3. label: 9
	4. patient: 9
	5. concomitant_drugs: 3
	6. concomitant_drugs/concomitant_drugs: 52
	7. concomitant_drugs/ien: 52
	8. concomitant_drugs/last_fill_dt: 52 (DATE)
	9. concomitant_drugs/sig: 16
	10. date_md_notified: 7 (DATE)
	11. date_reported: 2 (DATE)
	12. date_time_of_event: 9 (DATE) **M**
	13. fda_question_1: 1
	14. fda_question_2: 1
	15. fda_question_3: 1
	16. fda_question_4: 1
	17. label: 9 **M**
	18. observer: 9 (POINTER) **M**
	19. occupation: 6
	20. other_related_history: 1
	21. pt_action_fda_report: 1
	22. pt_action_mfr_report: 1
	23. pt_action_rcpm_report: 1
	24. question_1: 7
	25. question_10: 6
	26. question_2: 6
	27. question_3: 6
	28. question_5: 6
	29. question_6: 6
	30. question_7: 6
	31. question_9: 6
	32. reactions: 9 **M**
	33. reactions/entered_by: 10 (POINTER)
	34. reactions/ien: 10
	35. reactions/reactions: 10 (POINTER)
	36. related_reaction: 9 (POINTER) **M**
	37. reporter_address1: 4
	38. reporter_city: 4
	39. reporter_name: 6
	40. reporter_phone: 4
	41. reporter_state: 4 (POINTER)
	42. reporter_zip: 4
	43. reporting_user: 2 (POINTER)
	44. rpt_question_1: 6
	45. rpt_question_2: 6
	46. severity: 9 **M**
	47. suspected_agent: 9 **M**
	48. suspected_agent/ien: 9
	49. suspected_agent/suspected_agent: 9

3. GMRV VITAL MEASUREMENT-120_5 (132259) - 1394144 assertions

... mandatory properties: 10/15 - _id, date_time_vitals_entered, date_time_vitals_taken, entered_by, hospital_location, label, patient, rate, type, vital_type

	1. _id: 132259
	2. type: 132259
	3. label: 132259
	4. patient: 132259
	5. date_time_vitals_entered: 132259 (DATE) **M**
	6. date_time_vitals_taken: 132259 (DATE) **M**
	7. entered_by: 132259 (POINTER) **M**
	8. entered_in_error: 1216
	9. error_entered_by: 1216 (POINTER)
	10. hospital_location: 132259 (POINTER) **M**
	11. label: 132259 **M**
	12. qualifier: 22123
	13. qualifier/ien: 30793
	14. qualifier/qualifier: 30793 (POINTER)
	15. rate: 132259 **M**
	16. reason_entered_in_error: 1216
	17. reason_entered_in_error/date_reason_entered_in_error: 100 (DATE)
	18. reason_entered_in_error/ien: 1216
	19. reason_entered_in_error/reason_entered_in_error: 1216
	20. supplemental_o2: 5004
	21. vital_type: 132259 (POINTER) **M**

4. PATIENT ALLERGIES-120_8 (86) - 23300 assertions

... mandatory properties: 12/24 - _id, allergy_type, gmr_allergy, label, mechanism, observed_historical, origination_date_time, originator, originator_sign_off, patient, reactant, type

	1. _id: 86
	2. type: 86
	3. label: 86
	4. patient: 86
	5. allergy_type: 86 **M**
	6. chart_marked: 57
	7. chart_marked/date_time: 67 (DATE)
	8. chart_marked/ien: 67
	9. chart_marked/user_entering: 67 (POINTER)
	10. comments: 43
	11. comments/comment_type: 55
	12. comments/comments: 55
	13. comments/date_time_comment_entered: 55 (DATE)
	14. comments/ien: 55
	15. comments/user_entering: 55 (POINTER)
	16. date_time_entered_in_error: 20 (DATE)
	17. drug_classes: 69
	18. drug_classes/ien: 84
	19. drug_classes/va_drug_class: 84 (POINTER)
	20. drug_ingredients: 70
	21. drug_ingredients/drug_ingredient: 153 (POINTER)
	22. drug_ingredients/ien: 153
	23. entered_in_error: 20
	24. gmr_allergy: 86 (POINTER) **M**
	25. id_band_marked: 84
	26. id_band_marked/date_time: 6946 (DATE)
	27. id_band_marked/ien: 6946
	28. id_band_marked/user_entering: 6946 (POINTER)
	29. label: 86 **M**
	30. mechanism: 86 **M**
	31. observed_historical: 86 **M**
	32. origination_date_time: 86 (DATE) **M**
	33. originator: 86 (POINTER) **M**
	34. originator_sign_off: 86 **M**
	35. reactant: 86 **M**
	36. reactions: 61
	37. reactions/date_entered: 6 (DATE)
	38. reactions/entered_by: 69 (POINTER)
	39. reactions/ien: 71
	40. reactions/other_reaction: 2
	41. reactions/reaction: 71 (POINTER)
	42. user_entering_in_error: 20 (POINTER)
	43. verification_date_time: 83 (DATE)
	44. verified: 83
	45. verifier: 35 (POINTER)

5. PATIENT-2 (20) - 117894 assertions

... mandatory properties: 83/273 - _id, address_change_dt_tm, address_change_site, address_change_source, address_change_user, agent_orange_expos_indicated, check_for_duplicate, city, country, county, covered_by_health_insurance, current_enrollment, date_entered_into_file, date_medicaid_last_asked, date_of_birth, designee_change_date_time, disposition_login_date_time, dname_components, dname_of_designee, dphone_number, econtact_change_date_time, eligibility_status, eligibility_status_date, eligibility_status_entered_by, eligibility_verif_method, eligibility_verif_source, eligible_for_medicaid, employment_status, ename, ename_components, ephone_number, ethnicity_information, full_icn, kname_components, kname_of_primary_nok, kphone_number, label, laboratory_reference, language_date_time, marital_status, military_service_episode, mothers_maiden_name, mothers_maiden_name_components, name, name_components, pat_no, patient_eligibilities, pension_indicator_lock, period_of_service, place_of_birth_city, place_of_birth_state, preferred_facility, primary_eligibility_code, primary_long_id, primary_nok_change_date_time, primary_short_id, race_information, radiation_exposure_indicated, receiving_a_va_pension, receiving_aa_benefits, receiving_housebound_benefits, receiving_va_disability, religious_preference, residence_number_change_dt_tm, residence_number_change_site, residence_number_change_source, service_connected, sex, social_security_number, source_designation, southwest_asia_conditions, spinal_cord_injury, state, street_address_line_1, temporary_address_active, type, type_391, user_enrollee_site, user_enrollee_valid_through, veteran_y_n, who_entered_patient, zip4, zip_code

	1. _id: 20
	2. type: 20
	3. label: 20
	4. name: 20
	5. _2nd_most_recent_date_of_care: 1 (DATE)
	6. _2nd_most_recent_location: 1 (POINTER)
	7. address_change_dt_tm: 20 (DATE) **M**
	8. address_change_site: 20 (POINTER) **M**
	9. address_change_source: 20 **M**
	10. address_change_user: 20 (POINTER) **M**
	11. agent_orange_expos_indicated: 20 **M**
	12. agent_orange_exposure_location: 2
	13. alias: 2
	14. alias/alias: 3
	15. alias/alias_components: 3 (POINTER)
	16. alias/alias_ssn: 2
	17. alias/ien: 3
	18. amount_of_gi_insurance: 1
	19. amount_of_military_retirement: 1
	20. amount_of_social_security: 1
	21. amount_of_va_disability: 3
	22. appointment: 14
	23. appointment/appointment_date_time: 6814 (DATE)
	24. appointment/appointment_type: 6812 (POINTER)
	25. appointment/appointment_type_subcategory: 5249 (POINTER)
	26. appointment/appt_cancelled: 111 (POINTER)
	27. appointment/autorebooked_appt_date_time: 105 (DATE)
	28. appointment/cancellation_reason: 1315 (POINTER)
	29. appointment/cancellation_remarks: 1138
	30. appointment/clinic: 6814 (POINTER)
	31. appointment/data_entry_clerk: 4251 (POINTER)
	32. appointment/date_appt_made: 6573 (DATE)
	33. appointment/desired_date_of_appointment: 5540 (DATE)
	34. appointment/ekg_date_time: 7 (DATE)
	35. appointment/encounter_forms_as_addons: 54
	36. appointment/encounter_forms_printed: 672
	37. appointment/followup_visit: 5519
	38. appointment/ien: 6814
	39. appointment/lab_date_time: 95 (DATE)
	40. appointment/next_ava_appt_indicator: 6534
	41. appointment/noshow_cancel_date_time: 1750 (DATE)
	42. appointment/noshow_cancelled_by: 1750 (POINTER)
	43. appointment/outpatient_encounter: 5005 (POINTER)
	44. appointment/purpose_of_visit: 6814
	45. appointment/routing_slip_print_date: 2692 (DATE)
	46. appointment/routing_slip_printed: 2688
	47. appointment/scheduling_request_type: 6452
	48. appointment/status: 2578
	49. appointment/xray_date_time: 12 (DATE)
	50. appointment_request_comment: 4
	51. appointment_request_date: 9 (DATE)
	52. appointment_request_on_1010ez: 10
	53. appointment_request_status: 4
	54. attending_physician: 7 (POINTER)
	55. category_of_beneficiary: 17 (POINTER)
	56. cd_descriptors: 2
	57. cd_descriptors/cd_descriptors: 2 (POINTER)
	58. cd_descriptors/ien: 2
	59. cd_history_date: 19
	60. cd_history_date/cd_history_date: 794 (DATE)
	61. cd_history_date/cd_reason: 466
	62. cd_history_date/cd_reason/affected_extremity: 422
	63. cd_history_date/cd_reason/cd_reason: 677 (POINTER)
	64. cd_history_date/cd_reason/ien: 677
	65. cd_history_date/date_of_decision: 466 (DATE)
	66. cd_history_date/decided_by: 466
	67. cd_history_date/facility_making_determination: 466 (POINTER)
	68. cd_history_date/ien: 794
	69. cd_history_date/method_of_determination: 466
	70. cd_history_date/review_date: 466 (DATE)
	71. cd_history_date/veteran_catastrophically_disabled: 466
	72. cellular_number_change_dt_tm: 18 (DATE)
	73. cellular_number_change_site: 18 (POINTER)
	74. cellular_number_change_source: 18
	75. check_for_duplicate: 20 **M**
	76. city: 20 **M**
	77. claim_folder_location: 19 (POINTER)
	78. claim_number: 19
	79. cmor_activity_score: 15
	80. cmor_history: 4
	81. cmor_history/cmor_activity_score: 3
	82. cmor_history/cmor_change_date: 5 (DATE)
	83. cmor_history/cmor_history: 5
	84. cmor_history/cmor_score_calculation_date: 3 (DATE)
	85. cmor_history/ien: 5
	86. combat_from_date: 3 (DATE)
	87. combat_indicated_on_1010ez: 19
	88. combat_service_indicated: 19
	89. combat_service_location: 3 (POINTER)
	90. combat_to_date: 3 (DATE)
	91. confidential_addr_change_dt_tm: 2 (DATE)
	92. confidential_addr_change_site: 1 (POINTER)
	93. confidential_addr_country: 1 (POINTER)
	94. confidential_address_active: 2
	95. confidential_address_category: 1
	96. confidential_address_category/confidential_address_category: 1
	97. confidential_address_category/confidential_category_active: 1
	98. confidential_address_category/ien: 1
	99. confidential_address_city: 1
	100. confidential_address_county: 1
	101. confidential_address_state: 1 (POINTER)
	102. confidential_address_zip_code: 1
	103. confidential_end_date: 1 (DATE)
	104. confidential_start_date: 1 (DATE)
	105. confidential_street_line_1: 1
	106. country: 20 (POINTER) **M**
	107. county: 20 **M**
	108. covered_by_health_insurance: 20 **M**
	109. current_admission: 7 (POINTER)
	110. current_enrollment: 20 (POINTER) **M**
	111. current_health_benefit_plan: 1
	112. current_health_benefit_plan/assigned_date_and_time: 1 (DATE)
	113. current_health_benefit_plan/assigned_entered_by: 1 (POINTER)
	114. current_health_benefit_plan/current_hbp_code: 1 (POINTER)
	115. current_health_benefit_plan/current_source: 1
	116. current_health_benefit_plan/ien: 1
	117. current_means_test_status: 12 (POINTER)
	118. current_movement: 7 (POINTER)
	119. current_ph_indicator: 13
	120. current_purple_heart_remarks: 13
	121. current_room: 7 (POINTER)
	122. date_comment_last_edited: 4 (DATE)
	123. date_entered_into_file: 20 (DATE) **M**
	124. date_medicaid_last_asked: 20 (DATE) **M**
	125. date_of_birth: 20 (DATE) **M**
	126. date_of_decision: 2 (DATE)
	127. date_of_dental_treatment: 1
	128. date_of_dental_treatment/date_of_dental_treatment: 1 (DATE)
	129. date_of_dental_treatment/ien: 1
	130. date_of_retirement: 8 (DATE)
	131. date_status_last_edited: 4 (DATE)
	132. decided_by: 2
	133. dental_classification: 9 (POINTER)
	134. dental_eligibility_expiration: 2 (DATE)
	135. designee_change_date_time: 20 (DATE) **M**
	136. disability_ret_from_military: 17
	137. discharge_due_to_disability: 18
	138. disposition_login_date_time: 20 **M**
	139. disposition_login_date_time/amis_420_segment: 85 (POINTER)
	140. disposition_login_date_time/disposition: 97 (POINTER)
	141. disposition_login_date_time/elig_verified_at_registration: 93
	142. disposition_login_date_time/eligible_for_medicaid: 3
	143. disposition_login_date_time/facility_applying_to: 97 (POINTER)
	144. disposition_login_date_time/ien: 97
	145. disposition_login_date_time/log_in_date_time: 97 (DATE)
	146. disposition_login_date_time/log_out_date_time: 97 (DATE)
	147. disposition_login_date_time/need_related_to_an_accident: 97
	148. disposition_login_date_time/need_related_to_occupation: 96
	149. disposition_login_date_time/outpatient_encounter: 57 (POINTER)
	150. disposition_login_date_time/reason_for_late_disposition: 5 (POINTER)
	151. disposition_login_date_time/registration_eligibility_code: 93 (POINTER)
	152. disposition_login_date_time/sc_at_registration: 93
	153. disposition_login_date_time/status: 97
	154. disposition_login_date_time/type_of_benefit_applied_for: 97
	155. disposition_login_date_time/type_of_care_applied_for: 93
	156. disposition_login_date_time/who_dispositioned: 97 (POINTER)
	157. disposition_login_date_time/who_entered_10_10: 97 (POINTER)
	158. dname_components: 20 (POINTER) **M**
	159. dname_of_designee: 20 **M**
	160. dphone_number: 20 **M**
	161. e2contact_change_date_time: 5 (DATE)
	162. e2name_components: 5 (POINTER)
	163. e2name_of_secondary_contact: 5
	164. e2phone_number: 5
	165. econtact_change_date_time: 20 (DATE) **M**
	166. eff_date_combined_sc_eval: 13 (DATE)
	167. eligibility_status: 20 **M**
	168. eligibility_status_date: 20 (DATE) **M**
	169. eligibility_status_entered_by: 20 (POINTER) **M**
	170. eligibility_verif_method: 20 **M**
	171. eligibility_verif_source: 20 **M**
	172. eligible_for_medicaid: 20 **M**
	173. email_address: 5
	174. email_address_change_dt_tm: 5 (DATE)
	175. email_address_change_site: 5 (POINTER)
	176. email_address_change_source: 5
	177. email_address_indicator: 9
	178. email_address_indicator_dt_tm: 9 (DATE)
	179. employer_city: 6
	180. employer_name: 7
	181. employer_phone_number: 6
	182. employer_state: 6 (POINTER)
	183. employer_street_line_1: 4
	184. employer_street_line_2: 1
	185. employer_zip4: 4
	186. employer_zip_code: 4
	187. employment_status: 20 **M**
	188. ename: 20 **M**
	189. ename_components: 20 (POINTER) **M**
	190. enrollment_clinic: 19
	191. enrollment_clinic/current_status: 131
	192. enrollment_clinic/enrollment_clinic: 157 (POINTER)
	193. enrollment_clinic/enrollment_data: 156
	194. enrollment_clinic/enrollment_data/date_of_discharge: 148 (DATE)
	195. enrollment_clinic/enrollment_data/date_of_enrollment: 175 (DATE)
	196. enrollment_clinic/enrollment_data/ien: 175
	197. enrollment_clinic/enrollment_data/opt_or_ac: 155
	198. enrollment_clinic/enrollment_data/reason_for_discharge: 47
	199. enrollment_clinic/ien: 157
	200. ephone_number: 20 **M**
	201. ethnicity_information: 20 **M**
	202. ethnicity_information/ethnicity_information: 20 (POINTER)
	203. ethnicity_information/ien: 20
	204. ethnicity_information/method_of_collection: 20 (POINTER)
	205. exclude_from_facility_dir: 7
	206. facility_making_determination: 2 (POINTER)
	207. fathers_name: 19
	208. fathers_name_components: 19 (POINTER)
	209. fmqlStopped: 5
	210. full_icn: 20 **M**
	211. full_icn_history: 4
	212. full_icn_history/full_icn_history: 4
	213. full_icn_history/ien: 4
	214. gi_insurance_policy: 17
	215. grenada_service_indicated: 14
	216. history_health_benefit_plan: 1
	217. history_health_benefit_plan/history_assignment: 1
	218. history_health_benefit_plan/history_entered_by: 1 (POINTER)
	219. history_health_benefit_plan/history_hbp_code: 1 (POINTER)
	220. history_health_benefit_plan/history_hbp_date_time: 1 (DATE)
	221. history_health_benefit_plan/history_source: 1
	222. history_health_benefit_plan/ien: 1
	223. insurance_type: 19
	224. insurance_type/comment__patient_policy: 15
	225. insurance_type/comment__subscriber_policy: 19
	226. insurance_type/comment__subscriber_policy/comment: 16
	227. insurance_type/comment__subscriber_policy/comment_date_time: 20 (DATE)
	228. insurance_type/comment__subscriber_policy/ien: 20
	229. insurance_type/comment__subscriber_policy/last_edited_by: 20 (POINTER)
	230. insurance_type/coordination_of_benefits: 78
	231. insurance_type/date_entered: 87 (DATE)
	232. insurance_type/date_last_edited: 87 (DATE)
	233. insurance_type/date_last_verified: 87 (DATE)
	234. insurance_type/date_of_source_of_information: 87 (DATE)
	235. insurance_type/eb_display_entry: 34 (POINTER)
	236. insurance_type/effective_date_of_policy: 87 (DATE)
	237. insurance_type/eiv_autoupdate: 73
	238. insurance_type/eligibility_benefit: 36
	239. insurance_type/eligibility_benefit/address_line_1: 15
	240. insurance_type/eligibility_benefit/address_line_2: 5
	241. insurance_type/eligibility_benefit/authorization_certification: 83 (POINTER)
	242. insurance_type/eligibility_benefit/city: 15
	243. insurance_type/eligibility_benefit/contact_information: 11
	244. insurance_type/eligibility_benefit/contact_information/communication_number: 21
	245. insurance_type/eligibility_benefit/contact_information/communication_qualifier: 21 (POINTER)
	246. insurance_type/eligibility_benefit/contact_information/ien: 21
	247. insurance_type/eligibility_benefit/contact_information/sequence: 21
	248. insurance_type/eligibility_benefit/coverage_level: 258 (POINTER)
	249. insurance_type/eligibility_benefit/eb_number: 561
	250. insurance_type/eligibility_benefit/eligibility_benefit_info: 561 (POINTER)
	251. insurance_type/eligibility_benefit/entity_id: 4
	252. insurance_type/eligibility_benefit/entity_id_code: 18 (POINTER)
	253. insurance_type/eligibility_benefit/entity_id_qualifier: 4 (POINTER)
	254. insurance_type/eligibility_benefit/entity_type: 18 (POINTER)
	255. insurance_type/eligibility_benefit/healthcare_services_delivery: 4
	256. insurance_type/eligibility_benefit/healthcare_services_delivery/benefit_quantity: 6
	257. insurance_type/eligibility_benefit/healthcare_services_delivery/ien: 6
	258. insurance_type/eligibility_benefit/healthcare_services_delivery/quantity_qualifier: 6 (POINTER)
	259. insurance_type/eligibility_benefit/healthcare_services_delivery/sequence: 6
	260. insurance_type/eligibility_benefit/healthcare_services_delivery/time_period_qualifier: 3 (POINTER)
	261. insurance_type/eligibility_benefit/healthcare_services_delivery/time_periods: 3
	262. insurance_type/eligibility_benefit/ien: 561
	263. insurance_type/eligibility_benefit/in_plan: 259 (POINTER)
	264. insurance_type/eligibility_benefit/insurance_type: 210 (POINTER)
	265. insurance_type/eligibility_benefit/monetary_amount: 261
	266. insurance_type/eligibility_benefit/name: 18
	267. insurance_type/eligibility_benefit/notes: 217
	268. insurance_type/eligibility_benefit/percent: 112
	269. insurance_type/eligibility_benefit/plan_coverage_description: 45
	270. insurance_type/eligibility_benefit/quantity: 13
	271. insurance_type/eligibility_benefit/quantity_qualifier: 13 (POINTER)
	272. insurance_type/eligibility_benefit/service_types: 520
	273. insurance_type/eligibility_benefit/service_types/ien: 1658
	274. insurance_type/eligibility_benefit/service_types/service_types: 1658 (POINTER)
	275. insurance_type/eligibility_benefit/state: 15 (POINTER)
	276. insurance_type/eligibility_benefit/subscriber_additional_info: 44
	277. insurance_type/eligibility_benefit/subscriber_additional_info/ien: 44
	278. insurance_type/eligibility_benefit/subscriber_additional_info/place_of_service: 44 (POINTER)
	279. insurance_type/eligibility_benefit/subscriber_additional_info/qualifier: 44 (POINTER)
	280. insurance_type/eligibility_benefit/subscriber_additional_info/sequence: 44
	281. insurance_type/eligibility_benefit/subscriber_dates: 174
	282. insurance_type/eligibility_benefit/subscriber_dates/date: 174
	283. insurance_type/eligibility_benefit/subscriber_dates/date_format: 174 (POINTER)
	284. insurance_type/eligibility_benefit/subscriber_dates/date_qualifier: 174 (POINTER)
	285. insurance_type/eligibility_benefit/subscriber_dates/ien: 174
	286. insurance_type/eligibility_benefit/subscriber_dates/sequence: 174
	287. insurance_type/eligibility_benefit/subscriber_reference_id: 10
	288. insurance_type/eligibility_benefit/subscriber_reference_id/ien: 10
	289. insurance_type/eligibility_benefit/subscriber_reference_id/reference_id: 10
	290. insurance_type/eligibility_benefit/subscriber_reference_id/reference_id_qualifier: 10 (POINTER)
	291. insurance_type/eligibility_benefit/subscriber_reference_id/sequence: 10
	292. insurance_type/eligibility_benefit/time_period_qualifier: 265 (POINTER)
	293. insurance_type/eligibility_benefit/zip: 15
	294. insurance_type/employer_claims_city: 2
	295. insurance_type/employer_claims_phone: 1
	296. insurance_type/employer_claims_state: 2 (POINTER)
	297. insurance_type/employer_claims_street_address: 1
	298. insurance_type/employer_claims_zip_code: 2
	299. insurance_type/employment_status: 6
	300. insurance_type/entered_by: 87 (POINTER)
	301. insurance_type/esghp: 14
	302. insurance_type/group_name: 12
	303. insurance_type/group_number: 12
	304. insurance_type/group_plan: 87 (POINTER)
	305. insurance_type/group_reference_information: 34
	306. insurance_type/group_reference_information/description: 3
	307. insurance_type/group_reference_information/ien: 35
	308. insurance_type/group_reference_information/ref_id_qualifier_group: 35 (POINTER)
	309. insurance_type/group_reference_information/reference_id_group: 35
	310. insurance_type/group_reference_information/sequence: 35
	311. insurance_type/ien: 87
	312. insurance_type/insurance_expiration_date: 43 (DATE)
	313. insurance_type/insurance_type: 87 (POINTER)
	314. insurance_type/insureds_branch: 52 (POINTER)
	315. insurance_type/insureds_city: 62
	316. insurance_type/insureds_dob: 82 (DATE)
	317. insurance_type/insureds_phone: 53
	318. insurance_type/insureds_sex: 85
	319. insurance_type/insureds_ssn: 49
	320. insurance_type/insureds_state: 62 (POINTER)
	321. insurance_type/insureds_street_1: 62
	322. insurance_type/insureds_street_2: 2
	323. insurance_type/insureds_zip: 62
	324. insurance_type/last_edited_by: 59 (POINTER)
	325. insurance_type/name_of_insured: 87
	326. insurance_type/patient_id: 26
	327. insurance_type/pharmacy_relationship_code: 6 (POINTER)
	328. insurance_type/primary_care_provider: 2
	329. insurance_type/pt_relationship__hipaa: 87
	330. insurance_type/pt_relationship_to_insured: 87
	331. insurance_type/requested_service_date: 36 (DATE)
	332. insurance_type/requested_service_type: 36 (POINTER)
	333. insurance_type/send_bill_to_employer: 1
	334. insurance_type/source_of_information: 87 (POINTER)
	335. insurance_type/stop_policy_from_billing: 16
	336. insurance_type/subscriber_id: 87
	337. insurance_type/subscribers_employer_name: 9
	338. insurance_type/verified_by: 59 (POINTER)
	339. insurance_type/whose_insurance: 87
	340. k2address_same_as_patients: 2
	341. k2name_components: 8 (POINTER)
	342. k2name_of_secondary_nok: 8
	343. k2phone_number: 8
	344. kname_components: 20 (POINTER) **M**
	345. kname_of_primary_nok: 20 **M**
	346. kphone_number: 20 **M**
	347. label: 20 **M**
	348. laboratory_reference: 20 (POINTER) **M**
	349. language_date_time: 20 **M**
	350. language_date_time/ien: 20
	351. language_date_time/language_date_time: 20 (DATE)
	352. language_date_time/preferred_language: 20
	353. lebanon_service_indicated: 14
	354. marital_status: 20 (POINTER) **M**
	355. medicaid_number: 1
	356. method_of_determination: 2
	357. military_disability_retirement: 18
	358. military_service_episode: 20 **M**
	359. military_service_episode/data_locked: 23
	360. military_service_episode/ien: 23
	361. military_service_episode/service_branch: 23 (POINTER)
	362. military_service_episode/service_component: 5
	363. military_service_episode/service_discharge_type: 23 (POINTER)
	364. military_service_episode/service_entry_date: 23 (DATE)
	365. military_service_episode/service_number: 23
	366. military_service_episode/service_separation_date: 23 (DATE)
	367. monetary_ben_verify_date: 16 (DATE)
	368. most_recent_date_of_care: 3 (DATE)
	369. most_recent_location_of_care: 5 (POINTER)
	370. mothers_maiden_name: 20 **M**
	371. mothers_maiden_name_components: 20 (POINTER) **M**
	372. mothers_name: 19
	373. mothers_name_components: 19 (POINTER)
	374. multiple_birth_indicator: 7
	375. name_components: 20 (POINTER) **M**
	376. network_identifier: 17
	377. occupation: 15
	378. panama_service_indicated: 14
	379. pat_no: 20 **M**
	380. patient_eligibilities: 20 **M**
	381. patient_eligibilities/eligibility: 28 (POINTER)
	382. patient_eligibilities/ien: 28
	383. patient_eligibilities/long_id: 28
	384. patient_eligibilities/short_id: 28
	385. pension_award_effective_date: 1 (DATE)
	386. pension_award_reason: 1 (POINTER)
	387. pension_indicator_lock: 20 **M**
	388. period_of_service: 20 (POINTER) **M**
	389. persian_gulf_service: 14
	390. ph_date_time_updated: 13
	391. ph_date_time_updated/ien: 13
	392. ph_date_time_updated/ph: 13
	393. ph_date_time_updated/ph_date_time_updated: 13 (DATE)
	394. ph_date_time_updated/ph_remarks: 13
	395. ph_date_time_updated/ph_user: 13
	396. ph_division: 1 (POINTER)
	397. phone_number_cellular: 17
	398. phone_number_residence: 19
	399. phone_number_work: 19
	400. place_of_birth_city: 20 **M**
	401. place_of_birth_state: 20 (POINTER) **M**
	402. pow_status_indicated: 16
	403. pow_status_verified: 16 (DATE)
	404. preferred_facility: 20 (POINTER) **M**
	405. primary_eligibility_code: 20 (POINTER) **M**
	406. primary_long_id: 20 **M**
	407. primary_nok_change_date_time: 20 (DATE) **M**
	408. primary_short_id: 20 **M**
	409. provider: 6 (POINTER)
	410. pt: 17
	411. pt_effective_date: 8 (DATE)
	412. race: 14 (POINTER)
	413. race_information: 20 **M**
	414. race_information/ien: 20
	415. race_information/method_of_collection: 20 (POINTER)
	416. race_information/race_information: 20 (POINTER)
	417. radiation_exposure_indicated: 20 **M**
	418. rated_disabilities_va: 14
	419. rated_disabilities_va/current_effective_date: 96 (DATE)
	420. rated_disabilities_va/disability_: 97
	421. rated_disabilities_va/extremity_affected: 36
	422. rated_disabilities_va/ien: 97
	423. rated_disabilities_va/original_effective_date: 96 (DATE)
	424. rated_disabilities_va/rated_disabilities_va: 97 (POINTER)
	425. rated_disabilities_va/service_connected: 97
	426. rated_incompetent: 19
	427. received_va_care_previously: 9
	428. receiving_a_va_pension: 20 **M**
	429. receiving_aa_benefits: 20 **M**
	430. receiving_housebound_benefits: 20 **M**
	431. receiving_military_retirement: 4
	432. receiving_social_security: 5
	433. receiving_sup_security_ssi: 2
	434. receiving_va_disability: 20 **M**
	435. religious_preference: 20 (POINTER) **M**
	436. remarks: 3
	437. residence_number_change_dt_tm: 20 (DATE) **M**
	438. residence_number_change_site: 20 (POINTER) **M**
	439. residence_number_change_source: 20 **M**
	440. review_date: 2 (DATE)
	441. roombed: 7
	442. sc_award_date: 8 (DATE)
	443. score_calculation_date: 15 (DATE)
	444. secondary_nok_change_date_time: 10 (DATE)
	445. service_branch_last: 19 (POINTER)
	446. service_branch_nntl: 1 (POINTER)
	447. service_branch_ntl: 2 (POINTER)
	448. service_component_last: 2
	449. service_component_nntl: 1
	450. service_component_ntl: 1
	451. service_connected: 20 **M**
	452. service_connected_percentage: 14
	453. service_dental_injury: 17
	454. service_discharge_type_last: 19 (POINTER)
	455. service_discharge_type_nntl: 1 (POINTER)
	456. service_discharge_type_ntl: 2 (POINTER)
	457. service_entry_date_last: 19 (DATE)
	458. service_entry_date_nntl: 1 (DATE)
	459. service_entry_date_ntl: 2 (DATE)
	460. service_number_last: 19
	461. service_number_nntl: 1
	462. service_number_ntl: 2
	463. service_second_episode: 19
	464. service_separation_date_last: 19 (DATE)
	465. service_separation_date_nntl: 1 (DATE)
	466. service_separation_date_ntl: 2 (DATE)
	467. service_teeth_extracted: 17
	468. service_third_episode: 3
	469. service_verification_date: 19 (DATE)
	470. sex: 20 **M**
	471. social_security_number: 20 **M**
	472. somalia_service_indicated: 12
	473. source_designation: 20 **M**
	474. southwest_asia_conditions: 20 **M**
	475. special_counseling: 1
	476. special_counseling/clinic_title: 1
	477. special_counseling/clinic_title/clinic_title: 2 (POINTER)
	478. special_counseling/clinic_title/date_discharged: 2 (DATE)
	479. special_counseling/clinic_title/ien: 2
	480. special_counseling/comments: 1
	481. special_counseling/counseled_by: 1 (POINTER)
	482. special_counseling/date_counseled: 1 (DATE)
	483. special_counseling/date_identified: 1 (DATE)
	484. special_counseling/entry_by: 1 (POINTER)
	485. special_counseling/ien: 1
	486. special_counseling/plan: 1
	487. special_counseling/special_counseling: 1
	488. spinal_cord_injury: 20 **M**
	489. spouses_emp_phone_number: 3
	490. spouses_emp_street_line_1: 4
	491. spouses_emp_street_line_2: 1
	492. spouses_emp_zip4: 4
	493. spouses_emp_zip_code: 4
	494. spouses_employer_name: 5
	495. spouses_employers_city: 5
	496. spouses_employers_state: 5 (POINTER)
	497. spouses_employment_status: 13
	498. spouses_occupation: 13
	499. ssn_verification_status: 19
	500. state: 20 (POINTER) **M**
	501. street_address_line_1: 20 **M**
	502. street_address_line_2: 4
	503. temporary_address_active: 20 **M**
	504. temporary_address_change_dt_tm: 18 (DATE)
	505. temporary_address_change_site: 18 (POINTER)
	506. temporary_address_country: 5 (POINTER)
	507. temporary_address_county: 2
	508. temporary_address_end_date: 2 (DATE)
	509. temporary_address_start_date: 2 (DATE)
	510. temporary_city: 2
	511. temporary_phone_number: 1
	512. temporary_state: 2 (POINTER)
	513. temporary_street_line_1: 2
	514. temporary_zip4: 2
	515. temporary_zip_code: 2
	516. total_annual_va_check_amount: 18
	517. treating_specialty: 7 (POINTER)
	518. type_391: 20 (POINTER) **M**
	519. unemployable: 19
	520. user_enrollee_site: 20 (POINTER) **M**
	521. user_enrollee_valid_through: 20 (DATE) **M**
	522. veteran_catastrophically_disabled: 2
	523. veteran_y_n: 20 **M**
	524. vietnam_from_date: 2 (DATE)
	525. vietnam_service_indicated: 17
	526. vietnam_to_date: 2 (DATE)
	527. ward_location: 7
	528. who_entered_patient: 20 (POINTER) **M**
	529. yugoslavia_service_indicated: 7
	530. zip4: 20 **M**
	531. zip_code: 20 **M**

6. PROBLEM-9000011 (871) - 21355 assertions

... mandatory properties: 16/37 - _id, condition, date_entered, date_last_modified, diagnosis, entered_by, facility, label, nmbr, patient_name, problem, provider_narrative, recording_provider, responsible_provider, status, type

	1. _id: 871
	2. type: 871
	3. label: 871
	4. patient_name: 871
	5. agent_orange_exposure: 266
	6. clinic: 774 (POINTER)
	7. coding_system: 346
	8. combat_veteran: 85
	9. condition: 871 **M**
	10. date_entered: 871 (DATE) **M**
	11. date_last_modified: 871 (DATE) **M**
	12. date_of_interest: 334 (DATE)
	13. date_of_onset: 100 (DATE)
	14. date_recorded: 481 (DATE)
	15. date_resolved: 129 (DATE)
	16. diagnosis: 871 (POINTER) **M**
	17. entered_by: 871 (POINTER) **M**
	18. facility: 871 (POINTER) **M**
	19. head_and_or_neck_cancer: 85
	20. ionizing_radiation_exposure: 266
	21. label: 871 **M**
	22. mapping_targets: 3
	23. mapping_targets/code: 3
	24. mapping_targets/code_date: 3 (DATE)
	25. mapping_targets/coding_system: 3
	26. mapping_targets/ien: 3
	27. military_sexual_trauma: 103
	28. nmbr: 871 **M**
	29. note_facility: 216
	30. note_facility/ien: 222
	31. note_facility/note: 219
	32. note_facility/note/author: 363 (POINTER)
	33. note_facility/note/date_note_added: 363 (DATE)
	34. note_facility/note/ien: 363
	35. note_facility/note/note_narrative: 363
	36. note_facility/note/note_nmbr: 363
	37. note_facility/note/status: 363
	38. note_facility/note_facility: 222 (POINTER)
	39. persian_gulf_exposure: 266
	40. priority: 26
	41. problem: 871 (POINTER) **M**
	42. provider_narrative: 871 (POINTER) **M**
	43. recording_provider: 871 (POINTER) **M**
	44. responsible_provider: 871 (POINTER) **M**
	45. service: 558 (POINTER)
	46. service_connected: 278
	47. shipboard_hazard__defense: 102
	48. snomed_ct_concept_code: 347
	49. snomed_ct_designation_code: 221
	50. snomed_cttoicd_map_status: 18
	51. status: 871 **M**


