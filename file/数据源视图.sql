USE [3rdRIS_hebwy]
GO

/****** Object:  View [dbo].[ExamView]    Script Date: 2021/6/11 16:10:08 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE VIEW [dbo].[ExamView] AS SELECT DISTINCT
	OrderQuery.Id AS OrderPKID,
	NEWID( ) AS OrderID,
	1 AS IsMainOrder,
	'138A4B9F-A807-4DB2-842D-AC6E0109DD4B' AS OrganizationID,
	Hospital.Name AS OrganizationName,
	'F04F15F6-D21F-4C81-B297-AC6E0109EDCFO' AS ObservationDeptID,
	OrderQuery.GlobalPatientId AS PatientID,
	OrderQuery.AccessionNumber,
	OrderQuery.InpatientNumber AS InPatientNO,
	( SELECT Description FROM Department WHERE id = OrderQuery.OrderDepartmentId ) AS RequestDeptName,
	OrderQuery.RegisterTime AS RegDate,
	OrderQuery.RegisterTime AS Recordingtime,
	OrderQuery.StudyDate AS ObservationDate,
	OrderQuery.StudyDate AS ObservationEndDate,
	OrderQuery.StudyDate AS QAachieveDate,
	OrderQuery.StudyId AS StudyInstanceUID,
	OrderQuery.BodyPartNames AS ExamBodyPart,
	OrderQuery.CheckItems AS AllProcedureName,
	( SELECT LastName + FirstName FROM dbo.Staff WHERE id = OrderQuery.ApplyDoctorId ) AS ProviderName,
	( SELECT LastName + FirstName FROM dbo.Staff WHERE id = OrderQuery.OrderDoctorID ) AS Register,
	( SELECT LastName + FirstName FROM dbo.Staff WHERE id = OrderQuery.CheckInDoctorId ) AS TechnicianName,
	( SELECT LastName + FirstName FROM dbo.Staff WHERE id = OrderQuery.ReportDoctorId ) AS ResultPrincipalName,
	( SELECT LastName + FirstName FROM dbo.Staff WHERE id = OrderQuery.LastModifierId ) AS ResultReviseName,
	SUBSTRING ( OrderQuery.AccessionNumber, 0, 3 ) AS ServiceSectID,
	OrderQuery.Age,
	OrderQuery.AgeUnit,
	OrderQuery.BodyPartIds,
CASE
		PatientType 
		WHEN 'OP' THEN
		'1000' 
		WHEN 'IH' THEN
		'2000' 
		WHEN 'EM' THEN
		'3000' 
		WHEN 'PE' THEN
		'4000' ELSE '5000' 
	END AS PatientClass,
	OrderQuery.PatientName AS Name,
	OrderQuery.SpellName AS NameSpell,
	OrderQuery.Gender AS Sex,
	OrderQuery.DateOfBirth AS BirthDate,
	OrderQuery.IDCard,
	OrderQuery.ReportId AS ReportID,
	OrderQuery.IsPositive AS AbnormalFlag,
CASE
		dbo.OrderQuery.Status 
		WHEN 'Arrived' THEN
		'Registered' 
		WHEN 'Studyed' THEN
		'QAFinished' 
		WHEN 'Reporting' THEN
		'ReportWriteFinish' 
		WHEN 'Reported' THEN
		'ReportAuditeFinish' 
		WHEN 'Distributed' THEN
		'ReportReviseFinish' ELSE 'other' 
	END AS ResultStatusCode,
CASE
		dbo.OrderQuery.Status 
		WHEN 'Arrived' THEN
		1020 
		WHEN 'Studyed' THEN
		2090 
		WHEN 'Reporting' THEN
		3050 
		WHEN 'Reported' THEN
		3080 
		WHEN 'Distributed' THEN
		4030 ELSE 1000 
	END AS ResultStatus,
	OrderQuery.Impression AS ImagingDiagnosis,
	CAST ( dbo.Report.IsCritical AS VARCHAR ( 10 ) ) AS CriticalValue,
	OrderQuery.Findings AS ImagingFinding,
	Report.IsReportPrinted AS ResultPrintCount,
	Report.SubmitDateTime AS PreliminaryEndDate,
	Report.LastUpdateTime AS ReviseEndDate,
	Report.ApproveDatetime AS AuditEndDate,
	Hospital.Name AS DiagnosticOrganizationName,
	'00000000-0000-0000-0000-000000000000' AS DiagnosticOrganization,
	Device.ExamRoom AS ObservationLocation,
	[Order].HisOrderCode AS PlacerOrderNO,
	[Order].TotalFee AS Charges,
CASE
		dbo.[Order].ChargeStatus 
		WHEN 'ChargeEnsured' THEN
		1 
		WHEN 'UnCharged' THEN
		0 ELSE 3 
	END AS ChargeFlag
	
FROM
	dbo.OrderQuery
	LEFT JOIN dbo.Report ON OrderQuery.ReportId = Report.Id
	LEFT JOIN dbo.Hospital ON OrderQuery.ServerNode = Hospital.ServerNode
	LEFT JOIN dbo.Device ON OrderQuery.DeviceId = Device.Id
	LEFT JOIN dbo.[Order] ON OrderQuery.Id = [Order].Id 
WHERE
	OrderQuery.Status IN ( 'Arrived', 'Studyed', 'Reporting', 'Reported', 'Distributed' )
GO

