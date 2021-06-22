/**
 * Data important for map configuration
 * Standard values that are called in case no user values are set
 */

const hereCredentials = {
  apikey: 'HhbKhQDPxyd4BXse_54NLVZqEXzE5yOxc6wuYiXChNc'
}

const mapCenter = {
  /** Standard value for mapCenter (Hamburg, Germany) if user refuses to disclose their location */
  lat: 53.55,
  lng: 10.00
}

const mapIcons = {
  bookIcon: "{{ url_for('static', filename='bookIcon.png') }}",
  userIcon: "{{ url_for('static', filename='userIcon.png') }}"
}

const userCoords = {
  /** Standard value for user Position for testing purposes */
  lat: 53.56,
  lng: 10.03
}