import { Notification, SnackbarTheme } from '@/store/snackbar'

export const notifications: Record<string, Notification> = {
  removeOrgSuccess: {
    message: 'Organisatie verwijderd.',
    theme: SnackbarTheme.success,
  },
  noAccessRights: {
    message:
      'Je mist de rechten om dit in te zien. Neem contact op met het Algoritmeregister als je denkt dat dit niet klopt.',
    theme: SnackbarTheme.error,
  },
  fetchMeErrorDisabled: {
    message:
      'Je account is nog niet geactiveerd. Neem contact op met het Algoritmeregister om je account te activeren.',
    theme: SnackbarTheme.error,
    duration: 10000,
  },
  fetchArchiveError: {
    message: 'Er is iets fout gegaan bij het ophalen van het archief.',
    theme: SnackbarTheme.error,
  },
  addUserErrorNotUniqueUsername: {
    message: 'Het aangegeven e-mailadres is al in gebruik.',
    theme: SnackbarTheme.error,
  },
  addUserErrorInvalidEmail: {
    message:
      'Het aangegeven e-mailadres heeft niet het juiste format. Deze hoort er als volgt uit te zien: naam@domein.nl',
    theme: SnackbarTheme.error,
  },
  addUserSuccess: {
    message: 'Gebruiker toegevoegd!',
    theme: SnackbarTheme.success,
  },
  updateUserSuccess: {
    message: 'Gebruiker aangepast',
    theme: SnackbarTheme.success,
  },
  removeUserSuccess: {
    message: 'Gebruiker verwijderd',
    theme: SnackbarTheme.success,
  },
  addOrgSuccess: {
    message: 'Organisatie toegevoegd',
    theme: SnackbarTheme.success,
  },
  updateOrgSuccess: {
    message: 'Organisatie opgeslagen',
    theme: SnackbarTheme.success,
  },
  fetchOverviewError: {
    message: 'Er is een fout opgetreden bij het ophalen van de algoritmes.',
    theme: SnackbarTheme.error,
  },
  fetchMetadataError: {
    message:
      'Er is een fout opgetreden bij het ophalen van het aanlevervoorschrift.',
    theme: SnackbarTheme.error,
  },
  fetchFormDataError: {
    message: 'Er is iets fout gegaan bij het opvragen van het algoritme.',
    theme: SnackbarTheme.error,
  },
  cannotFindAlgorithmError: {
    message:
      'Algoritme niet gevonden. U bent teruggestuurd naar uw homepagina.',
    theme: SnackbarTheme.error,
  },
  createSuccess: {
    message: 'Het algoritme is succesvol opgeslagen.',
    theme: SnackbarTheme.success,
  },
  createValidationError: {
    message:
      'Er is iets fout gegaan bij het aanmaken van het algoritme. De volgende velden geven een foutmelding:',
    theme: SnackbarTheme.error,
  },
  createGenericError: {
    message: 'Er is iets misgegaan bij het valideren van de formuliervelden.',
    theme: SnackbarTheme.error,
  },
  updateSuccess: {
    message: 'Het algoritme is succesvol opgeslagen.',

    theme: SnackbarTheme.success,
  },
  updateValidationError: {
    message:
      'Er is iets fout gegaan bij het opslaan van het algoritme. De volgende velden geven een foutmelding:',
    theme: SnackbarTheme.error,
  },
  updateGenericError: {
    message: 'Er is iets misgegaan bij het valideren van de formuliervelden.',
    theme: SnackbarTheme.error,
  },
  updateNoChanges: {
    message:
      'Er zijn geen wijzigingen ten opzichte van de huidige versie. Er wordt geen nieuwe versie aangemaakt.',
    theme: SnackbarTheme.success,
  },
  retractError: {
    message: 'Er is iets fout gegaan bij het intrekken van het algoritme.',
    theme: SnackbarTheme.error,
  },
  retractSuccess: {
    message: 'Dit algoritme is ingetrokken.',
    theme: SnackbarTheme.success,
  },
  publishError: {
    message: 'Er is iets fout gegaan bij het publiceren van het algoritme.',
    theme: SnackbarTheme.error,
  },
  publishSuccess: {
    message: 'Het algoritme is succesvol gepubliceerd.',
    theme: SnackbarTheme.success,
  },
  releaseError: {
    message: 'Er is iets fout gegaan bij het vrijgeven van het algoritme.',
    theme: SnackbarTheme.error,
  },
  releaseSuccess: {
    message: 'Het algoritme is succesvol vrijgegeven.',
    theme: SnackbarTheme.success,
  },
  releaseOnPublishedError: {
    message:
      'Dit algoritme kan niet worden vrijgegeven. Deze fout kan voorkomen als een gepubliceerd en ongewijzigd algoritme word vrijgegeven.',

    theme: SnackbarTheme.error,
  },
  previewError: {
    message: 'Er is iets fout gegaan bij het genereren van de voorbeeldpagina.',
    theme: SnackbarTheme.error,
  },
  removeError: {
    message: 'Er is iets fout gegaan bij het verwijderen van het algoritme.',
    theme: SnackbarTheme.error,
  },
  removeSuccess: {
    message: 'Het algoritme is succesvol verwijderd.',
    theme: SnackbarTheme.success,
  },
  noOrgSelectedError: {
    message: 'Er kan geen algoritme worden aangemaakt zonder een organisatie.',
    theme: SnackbarTheme.error,
  },
  unknownError: {
    message:
      'Een gedeelte van het proces is misgegaan. Probeer het opnieuw of ververs je scherm.',
    theme: SnackbarTheme.error,
  },
  fetchAlgorithmVersionsError: {
    message: 'Er is iets fout gegaan bij het ophalen van opgeslagen versies.',
    theme: SnackbarTheme.error,
  },
  archiveVersionSuccess: {
    message: 'De geselecteerde versie is gearchiveerd.',
    theme: SnackbarTheme.success,
  },
  archiveVersionError: {
    message: 'Er is iets fout gegaan bij het archiveren van de geselecteerde versie.',
    theme: SnackbarTheme.error,
  },
  unarchiveVersionSuccess: {
    message: 'De geselecteerde versie is gedearchiveerd.',
    theme: SnackbarTheme.success,
  },
  unarchiveVersionError: {
    message: 'Er is iets fout gegaan bij het dearchiveren van de geselecteerde versie.',
    theme: SnackbarTheme.error,
  },
}

// Dialogs are based on action_keys as given by the available action.
export interface ActionWarning {
  title: string
  content: string
}

export const dialogContent: Record<string, ActionWarning> = {
  publish: {
    title: 'je gaat publiceren',
    content: 'Weet u zeker dat u dit algoritme wilt publiceren?',
  },
  retract: {
    title: 'je gaat een algoritmebeschrijving intrekken',
    content:
      'Weet u zeker dat u de vrijgave van dit algoritme wilt intrekken? Het algoritme is dan niet meer zichtbaar voor publiek en word teruggestuurd naar de redacteur.',
  },
  release_to_2: {
    title: 'je gaat vrijgeven naar de goedkeurder',
    content:
      'Weet u zeker dat u deze algoritmebeschrijving wilt vrijgeven? Deze kan dan gepubliceerd worden door de goedkeurder.',
  },
  reject_to_1: {
    title: 'je gaat afkeuren',
    content:
      'Weet u zeker dat u deze algoritmebeschrijving wilt afkeuren? De redacteur kan deze dan weer aanpassen.',
  },
  release: {
    title: 'je gaat vrijgeven ter goedkeuring',
    content:
      'Weet u zeker dat u dit algoritme wilt vrijgeven? Het algoritme kan dan worden gepubliceerd door BZK.',
  },
  remove: {
    title: 'je gaat een beschrijving verwijderen',
    content:
      'Weet u zeker dat u dit algoritme wilt verwijderen? Het algoritme word volledig uit de database gehaald.',
  },
  showArchivedVersion: {
    title: 'je gaat een gearchiveerde versie inladen',
    content: 'U gaat een gearchiveerde versie van dit algoritme in het webformulier laden.',
  },
}

export const httpNotifications: Record<number, Notification> = {
  400: {
    message:
      '(400) Er is een fout opgetreden bij het verwerken van uw verzoek. Controleer de ingevoerde gegevens en probeer het opnieuw.',
    theme: SnackbarTheme.error,
  },
  401: {
    message:
      '(401) U moet ingelogd zijn om deze actie uit te voeren. Log in of registreer om toegang te krijgen.',
    theme: SnackbarTheme.error,
  },
  403: {
    message:
      '(403) U heeft geen toestemming om deze actie uit te voeren of toegang te krijgen tot deze bron.',
    theme: SnackbarTheme.error,
  },
  404: {
    message:
      '(404) Het algoritme dat u zoekt is niet gevonden. Controleer de zoekopdracht of ga terug naar het overzicht van algoritmes.',
    theme: SnackbarTheme.error,
  },
  500: {
    message:
      '(500) Er is een interne applicatiefout opgetreden. Neem contact op met de beheerder.',
    theme: SnackbarTheme.error,
  },
}
